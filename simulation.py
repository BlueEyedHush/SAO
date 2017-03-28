from graph import NodeState, Graph


def set_initial_nodes_on_fire(graph, init_nodes, transitions):
    # we will store initial fire in the very first element
    transitions[0] = list()
    for init_node in init_nodes:
        graph.nodes[init_node].state = NodeState.BURNING
        transitions[0].append((init_node, NodeState.BURNING))

    return transitions


def spreading_finished(graph):
    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.neighbors:
            if neighbor.state == NodeState.UNTOUCHED:
                return False
    return True


def assign_firefighters(graph, solution, solution_index, n, transitions):
    step = transitions.keys()[-1] + 1
    transitions[step] = list()

    placed_ff = 0
    while placed_ff < n and solution_index < graph.nodes_number:
        if graph.nodes[solution[solution_index]].state == NodeState.UNTOUCHED:
            graph.nodes[solution[solution_index]].state = NodeState.DEFENDED
            transitions[step].append((solution[solution_index], NodeState.DEFENDED))
            placed_ff += 1
        else:
            solution_index += 1
    return solution_index, transitions


def spread_fire(graph, transitions):
    step = transitions.keys()[-1] + 1
    transitions[step] = list()

    burning_nodes = graph.get_burning_nodes()
    for burning_node in burning_nodes:
        for neighbor in burning_node.neighbors:
            if neighbor.state == NodeState.UNTOUCHED:
                neighbor.state = NodeState.BURNING
                transitions[step].append((neighbor.id, NodeState.BURNING))

    return transitions


def evaluate_result(graph):
    result = 0
    for node in graph.nodes.values():
        if node.state != NodeState.BURNING:
            result += 1
    return result


def simulation(graph, solution, init_nodes, ff_per_step):
    # save nodes transitions to visualize the process
    transitions = dict()

    transitions = set_initial_nodes_on_fire(graph, init_nodes, transitions)

    solution_index = 0
    iterations = 0
    while not spreading_finished(graph):
        solution_index, transitions = assign_firefighters(graph, solution, solution_index, ff_per_step, transitions)
        transitions = spread_fire(graph, transitions)
        iterations += 1
    print "It took {} iterations for the fire to stop spreading".format(iterations)

    result = evaluate_result(graph)
    print "Result: {} (saved nodes)".format(result)

    return transitions, iterations, result
