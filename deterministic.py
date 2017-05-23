from heapq import nlargest

from graph import NodeState
from simulation import spreading_finished, spread_fire


def greedy_solution(graph, init_nodes, ff_per_step):
    def greedy_placement(graph, ff_per_step):

        # determine nodes, which are neighbors to the burning nodes
        # return `ff_per_step` nodes, which are neighbors to untouched nodes
        burning_nodes = graph.get_burning_nodes()
        bnodes_neighbors = set()
        for bnode in burning_nodes:
            for node in bnode.neighbors:
                bnodes_neighbors.add(node)

        # get nodes with highest degree in terms of untouched neighbors
        neighbors_degree = list()
        for node in bnodes_neighbors:
            degree = 0
            for neighbor in node.neighbors:
                if neighbor.state == NodeState.UNTOUCHED:
                    degree += 1
            neighbors_degree.append((node, degree))

        best_condidates = nlargest(ff_per_step, neighbors_degree, key=lambda (node, degree): degree)
        return [node for (node, degree) in best_condidates]

    solution = list()

    # set initial nodes on fire
    for init_node in init_nodes:
        graph.nodes[init_node].state = NodeState.BURNING

    while not spreading_finished(graph):

        # determine firefighters positions
        ff_placement = greedy_placement(graph, ff_per_step)
        solution.extend(ff_placement)

        # position firefighters
        for node in ff_placement:
            node.state = NodeState.DEFENDED

        # spread fire
        spread_fire(graph, transitions={1: 1})

    id_solution = [node.id for node in solution]

    # append solution with missing nodes
    # this is not needed as long as we assume that the solution is not a permutation
    for i in xrange(len(graph.get_nodes())):
        if i not in id_solution:
            id_solution.append(i)
    return id_solution
