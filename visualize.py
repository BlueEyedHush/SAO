import matplotlib.pyplot as plt
import networkx as nx

from graph import NodeState


def on_key(event, args):
    if event.key == 'right':
        draw_next_step(args)

    elif event.key == 'left':
        draw_previous_step(args)

    elif event.key == 'q':
        exit(0)


def draw_graph(graph, untouched_nodes, burning_nodes, defended_nodes, edges, positions, labels, solution):
    node_size = 300
    labels_font_size = 12

    untouched_nodes_color = 'gray'
    defended_nodes_color = 'blue'
    burning_nodes_color = 'red'

    plt.clf()
    plt.axis('off')
    plt.title('Solution: ' + str(solution))

    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=burning_nodes,
                           node_size=node_size,
                           node_color=burning_nodes_color)
    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=defended_nodes,
                           node_size=node_size,
                           node_color=defended_nodes_color)
    nx.draw_networkx_nodes(graph,
                           pos=positions,
                           nodelist=untouched_nodes,
                           node_size=node_size,
                           node_color=untouched_nodes_color)

    nx.draw_networkx_edges(graph, pos=positions, edgelist=edges)
    nx.draw_networkx_labels(graph, pos=positions, labels=labels, font_size=labels_font_size)

    plt.show()


def draw_next_step(args):
    print "Drawing next step..."

    future_transitions = args['future_transitions']
    shown_transitions = args['shown_transitions']

    if future_transitions:

        step = future_transitions.keys()[0]
        transition = future_transitions.pop(step)
        shown_transitions.append(transition)

        for node_id, state in transition:
            if state == NodeState.BURNING:
                args['burning_nodes'].append(node_id)
                args['untouched_nodes'].remove(node_id)
            elif state == NodeState.DEFENDED:
                args['defended_nodes'].append(node_id)
                args['untouched_nodes'].remove(node_id)

        draw_graph(args['graph'], args['untouched_nodes'], args['burning_nodes'], args['defended_nodes'], args['edges'],
                   args['positions'], args['labels'], args['solution'])


def draw_previous_step(args):
    print "Not implemented yet :("


def visualize_simulation(graph, transitions, solution):
    nx_graph = nx.Graph()

    edges = graph.get_edges()
    nx_graph.add_edges_from(edges)
    positions = nx.spring_layout(nx_graph)

    labels = dict()
    for node_id in graph.nodes:
        labels[node_id] = node_id

    shown_transitions = list()

    untouched_nodes = list(graph.nodes)
    burning_nodes = list()
    defended_nodes = list()

    args = {
        'graph': nx_graph,
        'edges': edges,
        'positions': positions,
        'future_transitions': transitions,
        'shown_transitions': shown_transitions,
        'untouched_nodes': untouched_nodes,
        'burning_nodes': burning_nodes,
        'defended_nodes': defended_nodes,
        'labels': labels,
        'solution': solution,
    }

    plt.gcf().canvas.mpl_connect('key_press_event', lambda event: on_key(event, args))
    draw_graph(nx_graph, graph.nodes, None, None, edges, positions, labels, solution)
