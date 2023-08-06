from logging import warning
import math
import paml
import uml

from paml_check.constraints import \
    binary_temporal_constraint, \
    fork_constraint, \
    join_constraint, \
    unary_temporal_constaint, \
    anytime_before, \
    determine_time_constraint, \
    duration_constraint
from paml_check.utils import Interval
# from paml_check.minimize_duration import MinimizeDuration
from paml_check.convert_constraints import ConstraintConverter

import paml_time as pamlt # May be unused but is required to access paml_time values

import pysmt

class TimeVariable:
    def __init__(self, prefix, ref):
        self.ref = ref
        self.prefix = prefix
        self.name = f"{prefix}:{ref.identity}"
        self.symbol = pysmt.shortcuts.Symbol(self.name, pysmt.shortcuts.REAL)
        self.value = None

class TimeVariableGroup(dict):
    DURATION_VARIABLE = 'duration'
    START_TIME_VARIABLE = 'start'
    END_TIME_VARIABLE = 'end'

    @property
    def start(self):
        return self[self.START_TIME_VARIABLE]

    @property
    def end(self):
        return self[self.END_TIME_VARIABLE]

    @property
    def duration(self):
        return self[self.DURATION_VARIABLE]

    def _define_time_variable(self, prefix, ref):
        self[prefix] = TimeVariable(prefix, ref)

    def __init__(self, ref):
        self._define_time_variable(self.START_TIME_VARIABLE, ref)
        self._define_time_variable(self.END_TIME_VARIABLE, ref)
        self._define_time_variable(self.DURATION_VARIABLE, ref)


class Protocol:
    @property
    def identity(self):
        return self.ref.identity

    @property
    def time_variables(self):
        return self.identity_to_time_variables(self.ref.identity)

    @property
    def initial_time_variables(self):
        return self.identity_to_time_variables(self.initial.identity)

    @property
    def final_time_variables(self):
        return self.identity_to_time_variables(self.final.identity)

    def __init__(self, ref: paml.Protocol, epsilon=0.0001, infinity=10e10):
        self.node_func_map = {
            uml.JoinNode: self._insert_join,
            uml.ForkNode: self._insert_fork,
            uml.FlowFinalNode: self._insert_final,
            uml.InitialNode: self._insert_initial,
            uml.CallBehaviorAction: self._insert_call_behavior_action
        }
        self.edge_func_map = {
            uml.ControlFlow: self._insert_control_flow,
            uml.ObjectFlow: self._insert_object_flow
        }

        self.ref = ref
        self.epsilon = epsilon
        self.infinity = infinity

        self.control_flow = []
        self.object_flow = []


        self.initial = self.ref.initial()
        self.final = self.ref.final()

        self.forks = []
        self.joins = []

        # Build identity map
        self.identity_to_ref = {}
        self.identity_to_ref[self.initial.identity] = self.initial
        self.identity_to_ref[self.final.identity] = self.final
        for node in self.ref.nodes:
            self.identity_to_ref[ref.identity] = ref

        # Build time variables
        self.time_edges = []
        self.time_variable_groups = {}
        self.define_time_variable_group(self.initial)
        self.define_time_variable_group(self.final)
        for node in self.ref.nodes:
            self.define_time_variable_group(node)

        for node in self.ref.nodes:
            self._insert_activity_node(node)
        for edge in self.ref.edges:
            self._insert_activity_edge(edge)

        # Run these last since they depend on the object flow
        self.repair_nodes_with_no_in_flow()
        self.repair_nodes_with_no_out_flow()
        self.define_time_variable_group(self.ref)

    def collect_time_symbols(self):
        variables = []
        for _, grp in self.time_variable_groups.items():
            for _, v in grp.items():
                variables.append(v.symbol)
        return variables

    def define_time_variable_group(self, ref):
        self.time_variable_groups[ref.identity] = TimeVariableGroup(ref)
    
    def identity_to_time_variables(self, identity):
        org_identity = str(identity)
        while identity not in self.time_variable_groups:
            res = identity.rsplit('/', 1)
            if len(res) == 1:
                break
            identity = res[0]
        if identity not in self.time_variable_groups:
            raise Exception(f"Failed to find node for {org_identity}")
        return self.time_variable_groups[identity]

    def identity_to_node(self, identity):
        org_identity = str(identity)
        while identity not in self.identity_to_ref:
            res = identity.rsplit('/', 1)
            if len(res) == 1:
                break
            identity = res[0]
        if identity not in self.identity_to_ref:
            raise Exception(f"Failed to find node for {org_identity}")
        return self.identity_to_ref[identity]

    def _insert_activity_node(self, node):
        tvs = self.identity_to_time_variables(node.identity)
        if isinstance(node, uml.ExecutableNode):
            self._insert_time_edge(tvs.start, tvs.end, self.epsilon)
        else:
            self._insert_time_edge(tvs.start, tvs.end, 0)
        # Handle any type specific inserts
        t = type(node)
        if t not in self.node_func_map:
            warning(f"Skipping processing of node {node.identity}. No handler function found.")
            return
        self.node_func_map[t](node)

    def _insert_activity_edge(self, edge):
        # Handle any type specific inserts
        t = type(edge)
        if t not in self.edge_func_map:
            warning(f"Skipping processing of edge {edge.identity}. No handler function found.")
            return
        self.edge_func_map[t](edge)

    def _insert_control_flow(self, edge):
        self.control_flow.append(edge)

    def _insert_object_flow(self, edge):
        self.object_flow.append(edge)
        source = self.identity_to_time_variables(str(edge.source))
        target = self.identity_to_time_variables(str(edge.target))
        self._insert_time_edge(source.end, target.start, 0)

    def _insert_time_edge(self, start, end, min_d):
        difference = [[min_d, math.inf]]
        if start.value and end.value:
            d = end.value - start.value
            difference.append([d, d])
        intersected_difference = Interval.intersect(difference)
        self.time_edges.append((start, [intersected_difference], end))

    def _insert_join(self, node):
        v = self.identity_to_time_variables(node.identity)
        self.joins.append(v.start)

    def _insert_fork(self, node):
        v = self.identity_to_time_variables(node.identity)
        self.forks.append(v.end)

    def _insert_initial(self, node):
        self._insert_fork(node)

    def _insert_final(self, node):
        self._insert_join(node)

    def _insert_call_behavior_action(self, node):
        pass # We currently don't use these for anything type specific
        
    def find_fork_groups(self):
        fork_groups = {f: [] for f in self.forks}
        for (start, _, end) in self.time_edges:
            if start in fork_groups:
                fork_groups[start].append(end)
        return fork_groups

    def find_join_groups(self):
        join_groups = {j: [] for j in self.joins}
        for (start, _, end) in self.time_edges:
            if end in join_groups:
                join_groups[end].append(start)
        return join_groups

    def extract_time_constraints(self):
        cc = ConstraintConverter(self)
        protocol = self.ref
        doc = protocol.document
        count = len(protocol.time_constraints)

        # no constraints were specified
        if count == 0:
            # FIXME what shortcut is approriate to return when no constraints are specified?
            return pysmt.shortcuts.TRUE()

        # exactly one constraint was specified
        if count == 1:
            tc = doc.find(protocol.time_constraints[0])
            return cc.convert_constraint(tc)

        # more than one constraint was specified
        # so fallback to an implicit And
        warning(f"Protocol with identity '{protocol.indentity}' provided multiple top level constraints."
                + "\n  These will be treated as an implicit And operation. This is not recommended.")
        clauses = [ cc.convert_constraint(doc.find(tc_ref))
                    for tc_ref in protocol.time_constraints ]
        return pysmt.shortcuts.And(clauses)
        
    def _make_protocol_constraints(self):
        protocol_start = self.time_variables.start.symbol
        protocol_end = self.time_variables.end.symbol
        initial_start = self.initial_time_variables.start.symbol
        final_end = self.final_time_variables.end.symbol
        start_constraint = pysmt.shortcuts.Equals(protocol_start, initial_start)
        end_constraint = pysmt.shortcuts.Equals(protocol_end, final_end)
        return [start_constraint, end_constraint, self.extract_time_constraints()]

    def generate_constraints(self):
        symbols = self.collect_time_symbols()
        protocol_constraints = self._make_protocol_constraints()

        timepoint_var_domains = [pysmt.shortcuts.And(pysmt.shortcuts.GE(s, pysmt.shortcuts.Real(0.0)),
                                                     pysmt.shortcuts.LE(s, pysmt.shortcuts.Real(self.infinity)))
                                 for s in symbols]

        time_constraints = [binary_temporal_constraint(start.symbol,
                                                       Interval.substitute_infinity(self.infinity, disjunctive_distance),
                                                       end.symbol)
                            for (start, disjunctive_distance, end) in self.time_edges]
        
        join_constraints = []                     
        join_groups = self.find_join_groups()
        for j, grp in join_groups.items():
            join_constraints.append(
                join_constraint(
                    j.symbol,
                    [v.symbol for v in grp]
                )
            )

        fork_constraints = []                     
        fork_groups = self.find_fork_groups()
        for f, grp in fork_groups.items():
            fork_constraints.append(
                fork_constraint(
                    f.symbol,
                    [v.symbol for v in grp]
                )
            )

        return pysmt.shortcuts.And( \
            timepoint_var_domains + \
            time_constraints + \
            join_constraints + \
            fork_constraints + \
            protocol_constraints \
        )

    # TODO remove once final nodes are provided in document
    def repair_nodes_with_no_out_flow(self):
        final = self.identity_to_time_variables(self.final.identity)
        results = []
        for node in self.ref.nodes:
            found = False
            for edge in self.object_flow:
                source = self.identity_to_time_variables(str(edge.source))
                if source.end.ref == node:
                    found = True
                    break
            if found is False:
                results.append(self.identity_to_time_variables(node.identity))
        if len(results) > 0:
            warning("Repairing out flow")
            for result in results:
                if isinstance(result.end.ref, uml.InitialNode):
                    continue
                if isinstance(result.end.ref, uml.FlowFinalNode):
                    continue
                warning(f"  {result.end.ref.identity}--->{final.start.ref.identity}")
                self._insert_time_edge(result.end, final.start, 0)

    # TODO remove once initial nodes are provided in document
    def repair_nodes_with_no_in_flow(self):
        initial = self.identity_to_time_variables(self.initial.identity)
        results = []
        for node in self.ref.nodes:
            found = False
            for edge in self.object_flow:
                target = self.identity_to_time_variables(str(edge.target))
                if target.start.ref == node:
                    found = True
                    break
            if found is False:
                results.append(self.identity_to_time_variables(node.identity))
        if len(results) > 0:
            warning("Repairing in flow")
            for result in results:
                if isinstance(result.start.ref, uml.InitialNode):
                    continue
                if isinstance(result.start.ref, uml.FlowFinalNode):
                    continue
                warning(f"  {initial.end.ref.identity}--->{result.start.ref.identity}")
                self._insert_time_edge(initial.end, result.start, 0)
    
    def print_debug(self):
        try:
            print("Control Flow")
            for edge in self.control_flow:
                print(f"  {edge.identity}")
            print("----------------")

            print("Object Flow")
            for edge in self.object_flow:
                print(f"  {edge.identity}")
            print("----------------")

            print("Time Edges")
            for edge in self.time_edges:
                print(f"  {edge[0].name} ---> {edge[2].name}")
            print("----------------")

            print("Joins")
            join_groups = self.find_join_groups()
            for j, grp in join_groups.items():
                print(f"  {j.name}")
                for v in grp:
                    print(f"    - {v.name}")
            print("----------------")

            print("Forks")
            fork_groups = self.find_fork_groups()
            for f, grp in fork_groups.items():
                print(f"  {f.name}")
                for v in grp:
                    print(f"    - {v.name}")
            print("----------------")
        except Exception as e:
            print(f"Error during print_debug: {e}")
    

    def print_variables(self, model):
        print("Time Variables")
        for name, grp in self.time_variable_groups.items():
            print(f"  {name}")
            for _, var in grp.items():
                print(f"    {var.prefix} = {float(model[var.symbol].constant_value())}")
        print("----------------")
