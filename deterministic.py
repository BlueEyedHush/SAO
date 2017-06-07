from heapq import nlargest

from graph import NodeState, Tree
from simulation import spreading_finished, spread_fire, simulation
from visualize import visualize_simulation


def untouched_subtree(node):
    """ Returns the size of UNTOUCHED (sub)tree
     that can be reached without crossing any BURNING or DEFENDED nodes """

    if not node:
        return 0

    if node.state == NodeState.UNTOUCHED:
        node_degree = 1
    else:
        return 0

    nodes = [node]

    while nodes:
        n = nodes.pop(0)
        if n.left and n.left.state == NodeState.UNTOUCHED:
            node_degree += 1
            nodes.append(n.left)
        if n.right and n.right.state == NodeState.UNTOUCHED:
            node_degree += 1
            nodes.append(n.right)

    return node_degree


def parent_untouched_tree(node):
    """Return the size of UNTOUCHED tree that is located 'above' of the node
        and can be reached without crossing any BURNING or DEFENDED nodes"""
    if not node:
        return 0

    node_degree = 0

    parent = node.parent
    while parent and parent.state == NodeState.UNTOUCHED:
        node_degree += 1
        if parent.left and parent.left == node:
            # add right subtree to calculations
            node_degree += untouched_subtree(parent.right)
        if parent.right and parent.right == node:
            # add left subtree to calculations
            node_degree += untouched_subtree(parent.left)

        node = parent
        parent = parent.parent

    return node_degree


def greedy_tree_solution(graph, init_nodes, ff_per_step):
    def greedy_placement(graph, ff_per_step):

        # get nodes with highest degree in terms of untouched neighbors
        neighbors_degree = list()
        burning_nodes = graph.get_burning_nodes()
        for bnode in burning_nodes:

            if bnode.parent:
                neighbors_degree.append((bnode.parent, parent_untouched_tree(bnode)))
            if bnode.left:
                neighbors_degree.append((bnode.left, untouched_subtree(bnode.left)))
            if bnode.right:
                neighbors_degree.append((bnode.right, untouched_subtree(bnode.right)))

        best_candidates = nlargest(ff_per_step, neighbors_degree, key=lambda (node, degree): degree)
        return [node for (node, degree) in best_candidates]

    # TODO: a lot of common code with the other deterministic approach
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


def greedy_solution(graph, init_nodes, ff_per_step):
    def greedy_placement(graph, ff_per_step):

        # determine nodes, which are neighbors to the burning nodes
        # return `ff_per_step` nodes, which are neighbors to untouched nodes
        burning_nodes = graph.get_burning_nodes()
        bnodes_neighbors = set()
        for bnode in burning_nodes:
            for node in bnode.get_neighbors():
                bnodes_neighbors.add(node)

        # get nodes with highest degree in terms of untouched neighbors
        neighbors_degree = list()
        for node in bnodes_neighbors:
            degree = 0
            for neighbor in node.get_neighbors():
                if neighbor.state == NodeState.UNTOUCHED:
                    degree += 1
            neighbors_degree.append((node, degree))

        best_candidates = nlargest(ff_per_step, neighbors_degree, key=lambda (node, degree): degree)
        return [node for (node, degree) in best_candidates]

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
