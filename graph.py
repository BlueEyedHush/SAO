from enum import Enum


class Graph(object):
    def __init__(self):
        self.nodes_number = 0
        self.nodes = dict()
        self.starting_nodes = list()
        super(Graph, self).__init__()

    def get_burning_nodes(self):
        bnodes = set()
        for node_id in self.nodes:
            if self.nodes[node_id].state == NodeState.BURNING:
                bnodes.add(node_id)
        return bnodes

    def get_starting_nodes(self):
        return self.starting_nodes

    def from_file(self, input_file):
        """ Generate graph from file format:
        n m s
        1 4
        1 2
        2 3
        ...
        where n is the number of vertices, m number of edges and s number of starting vertices
        next line lists starting vertices
        and the following lines determine edges
        this is exactly the format generated by the generate utility
        """
        with open(input_file, 'r') as f:
            self.nodes_number, _ = map(int, f.readline().split())
            self.starting_nodes = f.readline().split()
            self.starting_nodes = [Node(s) for s in self.starting_nodes]
            for node_id in xrange(self.nodes_number):
                self.nodes[node_id] = Node(node_id)
            for line in f:
                v1, v2 = line.split()
                v1, v2 = Node(v1), Node(v2)
                v1.add_neighbor(v2)
        return self.starting_nodes


class Node(object):
    def __init__(self, node_id, value=None):
        self.id = node_id
        self.neighbors = set()
        self.state = NodeState.UNTOUCHED
        self.value = value
        super(Node, self).__init__()

    def add_neighbor(self, node):
        self.neighbors.add(node)
        node.neighbors.add(self)

    def print_graph(self):
        """ Print the graph structure accessible from this node """
        raise NotImplementedError

    def __eq__(self, other):
        return self.id == other.id


NodeState = Enum('UNTOUCHED', 'DEFENDED', 'BURNING')
