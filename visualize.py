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

        plt.clf()
        plt.axis('off')

        nx.draw_networkx_nodes(args['graph'],
                               pos=args['positions'],
                               nodelist=args['burning_nodes'],
                               node_size=args['node_size'],
                               node_color='y')

        nx.draw_networkx_nodes(args['graph'],
                               pos=args['positions'],
                               nodelist=args['defended_nodes'],
                               node_size=args['node_size'],
                               node_color='b')

        nx.draw_networkx_nodes(args['graph'],
                               pos=args['positions'],
                               nodelist=args['untouched_nodes'],
                               node_size=args['node_size'],
                               node_color='r')

        nx.draw_networkx_edges(args['graph'], pos=args['positions'], edgelist=args['edges'], node_color='r')

        plt.show()


def draw_previous_step(args):
    print "Not implemented yet :("


def visualize_simulation(graph, transitions):
    NODE_SIZE = 300

    G = nx.Graph()
    edges = graph.get_edges()
    G.add_edges_from(edges)
    positions = nx.spring_layout(G)
    nx.draw(G, pos=positions)

    shown_transitions = list()

    untouched_nodes = list(graph.nodes)
    burning_nodes = list()
    defended_nodes = list()

    args = {
        'graph': G,
        'edges': edges,
        'positions': positions,
        'future_transitions': transitions,
        'shown_transitions': shown_transitions,
        'untouched_nodes': untouched_nodes,
        'burning_nodes': burning_nodes,
        'defended_nodes': defended_nodes,
        'node_size': NODE_SIZE,
    }

    plt.gcf().canvas.mpl_connect('key_press_event', lambda event: on_key(event, args))
    plt.axis('off')
    plt.show()
