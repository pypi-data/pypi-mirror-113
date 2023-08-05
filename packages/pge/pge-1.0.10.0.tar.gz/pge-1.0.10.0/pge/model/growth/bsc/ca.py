import networkx as nx
import numpy as np

from pge.model.growth.bsc.basic import BasicGrowth


class CAGrowth(BasicGrowth):
    def __init__(self, graph, deg, params):
        super().__init__(graph, deg, params)
        self.param = params

    def prep(self, graph):
        rs = nx.clustering(graph.get_nx_graph())
        graph.set_attrs("clust", {k: 0 if v is np.NaN else v for k, v in rs.items()})
        return graph

    def choice(self, graph, sz, tp="in"):
        nodes = graph.get_ids(stable=True)
        probs = graph.get_attributes("clust") ** self.param[0] + self.param[1]

        nodes, probs = nodes[probs > 0], probs[probs > 0]
        if probs.size == 0:
            return None
        probs = probs / np.sum(probs)
        return np.random.choice(nodes, sz, replace=False, p=probs)
