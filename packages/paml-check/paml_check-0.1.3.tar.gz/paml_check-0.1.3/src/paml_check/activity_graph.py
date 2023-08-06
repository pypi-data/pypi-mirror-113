from logging import warning
import math
import paml
import sbol3
import tyto
import uml

from paml_check.constraints import \
    binary_temporal_constraint, \
    fork_constraint, \
    join_constraint, \
    unary_temporal_constaint, \
    anytime_before, \
    determine_time_constraint, \
    duration_constraint
from paml_check.units import om_convert
from paml_check.utils import Interval
from paml_check.minimize_duration import MinimizeDuration
from paml_check.convert_constraints import ConstraintConverter
from paml_check.protocol import Protocol

import paml_time as pamlt # May be unused but is required to access paml_time values

import pysmt
import pysmt.shortcuts

class ActivityGraph:

    def __init__(self, doc: sbol3.Document, epsilon=0.0001, infinity=10e10, destructive=False):
        if destructive:
            self.doc = doc
        else:
            # TODO there may be a more efficient way to clone a sbol3 Document
            # write the original doc to a string and then read it in as a new doc
            self.doc = sbol3.Document()
            self.doc.read_string(doc.write_string('ttl'), 'ttl')

        self.epsilon = epsilon
        self.infinity = infinity
        self.variables = {}
        self.protocols = {}
        self._process_doc()

    def _process_doc(self):
        sbol3.set_namespace('https://bbn.com/scratch/')

        protocols = self.doc.find_all(lambda obj: isinstance(obj, paml.Protocol))
        # FIXME final_all seems to return duplicates
        p_count = len(protocols)
        protocols = list(set(protocols))
        if p_count != len(protocols):
            warning(("Removed duplicate protocols returned from find_all"))
        for protocol in protocols:
            print(f"Initializing protocol: {protocol.identity}")
            self.protocols[protocol.identity] = Protocol(protocol, self.epsilon, self.infinity)

    def print_debug(self):
        try:
            for _, protocol in self.protocols.items():
                print(f"Protocol: {protocol.identity}")
                protocol.print_debug()
        except Exception as e:
            print(f"Error during print_debug: {e}")

    def print_variables(self, model):
        try:
            print("Protocols")
            for _, protocol in self.protocols.items():
                print(f"Protocol: {protocol.identity}")
                protocol.print_variables(model)
            print("----------------")
        except Exception as e:
            print(f"Error during print_variables: {e}")


    def generate_constraints(self):
        protocol_constraints = []
        for _, protocol in self.protocols.items():
            protocol_constraints.append(protocol.generate_constraints())
        if len(protocol_constraints) == 1:
            return protocol_constraints[0]
        return pysmt.shortcuts.And(protocol_constraints)


    # def add_result(self, doc, result):
    #     if result:
    #         for var, value in result:
    #             v = float(value.constant_value())
    #             graph_node = self.var_to_node[var]
    #             doc_node = doc.find(graph_node) # FIXME use the self.uri_to_node, but fix it to include all the nodes
    #             doc_node.value = sbol3.Measure(v, tyto.OM.time)

    #     return doc

    def get_end_time_var(self, protocol):
        return self.protocols[protocol.identity].final_time_variables.end.symbol

    def get_duration(self, model, protocol):
        """
        Get the duration of protocol represented by model
        :param model:
        :return: value
        """
        duration = None
        if model:
            final_node_end_var = self.get_end_time_var(protocol)
            duration = float(model[final_node_end_var].constant_value())
        return duration


    # def compute_durations(self, doc):
    #     """
    #     Use start and end times on activities to compute their durations,
    #     including the overall protocol duration.
    #     :param doc:
    #     :return: doc
    #     """

    #     def calculate_duration(elt):
    #         return sbol3.Measure(elt.end.value.value - elt.start.value.value,
    #                              tyto.OM.time)

    #     for _, protocol in self.protocols.items():
    #         # set protocol start and end times
    #         protocol.start.value = sbol3.Measure(protocol.initial().start.value.value, tyto.OM.time)
    #         protocol.end.value = sbol3.Measure(protocol.final().end.value.value, tyto.OM.time)
    #         protocol.duration.value = calculate_duration(protocol)

    #     for _, activity in self.identity_to_node.items():
    #         if hasattr(activity, "duration") and \
    #            hasattr(activity, "start") and \
    #            hasattr(activity.start, "value") and \
    #            hasattr(activity, "end") and \
    #            hasattr(activity.end, "value"):
    #             activity.duration.value = calculate_duration(activity)
    #     return doc

    def get_minimum_duration(self):
        """
        Find the minimum duration for the protocol.
        Solver is SMT, so do a binary search on the duration bound.
        :return: minimum duration
        """

        base_formula = self.generate_constraints()
        result = pysmt.shortcuts.get_model(base_formula)
        min_duration = {protocol: None for protocol in self.protocols}
        if result:
            for _, protocol in self.protocols.items():
                # TODO push Protocol object through
                supremum_duration = self.get_duration(result, protocol.ref)
                min_duration[protocol] = MinimizeDuration(base_formula, self, protocol.ref).minimize(supremum_duration)

        return min_duration