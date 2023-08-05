import numpy as np

from pge.model.growth.bsc.basic import BasicGrowth
from pge.model.growth.bsc.basic_fix import FixUnGrowth


class PAGrowth(BasicGrowth):
    def prep(self, graph):
        graph.set_attrs(
            "dg_in", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        graph.set_attrs(
            "dg_out", {node: graph.count_out_degree(node) for node in graph.get_ids()}
        )
        return graph

    def choice(self, gr, sz, tp="in"):
        ids = gr.get_ids(stable=True)
        probs = gr.get_attributes("dg_" + tp) + self.param[tp != "in"]
        probs = probs / np.sum(probs)
        probs, ids = probs[probs > 0], ids[probs > 0]
        return np.random.choice(ids, sz, replace=False, p=probs)


class PAFixUnGrowth(FixUnGrowth):
    def choice(self, graph, sz):
        probs = graph.get_attributes("dg") + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(graph.get_ids(stable=True), sz, replace=False, p=probs)

    def clean(self, graph):
        graph = self.prep(graph)
        if self.param != 0:
            return []

        dels = graph.get_ids(stable=True)[(graph.get_attributes("dg") == 0)]
        return dels

    def prep(self, graph):
        graph.set_attrs(
            "dg", {node: graph.count_in_degree(node) for node in graph.get_ids()}
        )
        return graph
