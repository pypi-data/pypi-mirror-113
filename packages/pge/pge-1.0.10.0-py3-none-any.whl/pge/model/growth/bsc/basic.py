import numpy as np
import networkx as nx

from pge.init.classes.graph import SGraph


class BasicGrowth:
    def __init__(self, graph, deg, params):
        self.gr = graph
        self.deg = deg
        if graph.directed():
            self.param = params
        else:
            self.param = (params, )
        self.count = 0

    def choice(self, gr, sz, tp="in"):
        return []

    def new_edge_add(self, gr, attrs):
        node1, node2 = self.choice(gr, 1, tp="out")[0], self.choice(gr, 1, tp="in")[0]
        gr.add_edge(node1, node2, str(self.count), {attrs[0]: attrs[1] + 1})
        self.count += 1

    def new_node_add(self, graph, to, attrs, tp=None):
        if tp == 0:
            if self.deg[0][0] == "const":
                nodes = self.choice(graph, self.deg[0][1], tp="in")
            else:
                nodes = self.choice(graph, self.deg[0][0](self.deg[0][1]), tp="in")
        else:
            if self.deg[1][0] == "const":
                nodes = self.choice(graph, self.deg[1][1], tp="out")
            else:
                nodes = self.choice(graph, self.deg[1][0](self.deg[1][1]), tp="out")

        for node in nodes:
            if tp == 0:
                graph.add_edge(to, node, key=str(self.count), prms={attrs[0]: attrs[1] + 1})
            else:
                graph.add_edge(node, to, key=str(self.count), prms={attrs[0]: attrs[1] + 1})
            self.count += 1
        graph.set_attr(to, attrs[0], attrs[1] + 1)
        return nodes

    def prep(self, graph):
        return graph

    def make_copy(self, gr):
        return gr

    def proceed(self, n, save=None, attr="cnt"):
        if save is None:
            return None

    @staticmethod
    def save(gr, to):
        nx.write_graphml(gr.get_nx_graph(), to + ".graphml")

    def new_load(self, gr):
        return gr

    def stop(self):
        return False

    def add(self, graph):
        return


class SchemaGrowth(BasicGrowth):
    def __init__(self, graph, deg, params, schema):
        BasicGrowth.__init__(self, graph, deg, params)
        self.schema = schema

    def make_copy(self, gr):
        if gr.directed():
            graph = nx.MultiDiGraph()
        else:
            graph = nx.MultiGraph()

        count = 0
        for edge in gr.get_edges():
            graph.add_edge(edge[0], edge[1], key="old-"+str(count))
            count += 1
        return SGraph(graph)

    def proceed(self, n, save=None, attr="cnt"):
        self.count = 0
        nw_graph = self.make_copy(self.gr)
        nx.set_node_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nx.set_edge_attributes(nw_graph.get_nx_graph(), 0, name=attr)
        nw_graph = self.new_load(nw_graph)

        count = self.gr.size()
        for _ in np.arange(n):
            print(_)
            if self.stop():
                break

            nw_graph = self.prep(nw_graph)
            self.add(nw_graph)
            new_node = np.random.choice(len(self.schema), p=self.schema)
            if new_node == 1:
                self.new_edge_add(nw_graph, (attr, _))
            else:
                self.new_node_add(nw_graph, str(count), (attr, _), new_node)
                count += 1
        if save is None:
            return nw_graph
        else:
            self.save(nw_graph, save)


class SimpleGrowth(SchemaGrowth):
    def __init__(self, graph, deg, params):
        super(SchemaGrowth, self).__init__(graph, deg, params)
        self.schema = [1]

    def make_copy(self, gr):
        if gr.directed():
            graph = nx.DiGraph()
        else:
            graph = nx.Graph()

        count = 0
        for edge in gr.get_edges():
            graph.add_edge(edge[0], edge[1], key="old-" + str(count))
            count += 1
        return SGraph(graph)
