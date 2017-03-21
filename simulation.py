from graph import Graph, NodeState


def spreading_finished(graph):
    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.neighbors:
            if neighbor.state == NodeState.UNTOUCHED:
                return False
    return True


def assign_firefighters(graph, solution, solution_index, n):
    placed_ff = 0
    while placed_ff < n and solution_index < graph.nodes_number:
        if graph.nodes[solution[solution_index]].state == NodeState.UNTOUCHED:
            graph.nodes[solution[solution_index]].state = NodeState.DEFENDED
            placed_ff += 1
        else:
            solution_index += 1
    return solution_index


def spread_fire(graph):
    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.neighbors:
            if neighbor.state == NodeState.UNTOUCHED:
                neighbor.state = NodeState.BURNING


def evaluate_result(graph):
    result = 0
    for node in graph.nodes.values():
        if node.state != NodeState.BURNING:
            result += 1
    return result


def simulation(graph, solution, starting_nodes, ff_per_step):
    for sn in starting_nodes:
        graph.nodes[sn].state = NodeState.BURNING

    solution_index = 0
    iterations = 0
    while not spreading_finished(graph):
        solution_index = assign_firefighters(graph, solution, solution_index, ff_per_step)
        spread_fire(graph)
        iterations += 1
    print "It took {} iterations for the fire to stop spreading".format(iterations)

    result = evaluate_result(graph)
    print "Result: {} (saved nodes)".format(result)


g = Graph()
g.from_file('graphs/simple.txt')
solution = [1, 0, 3, 4, 2]
simulation(g, solution, [3], 1)
