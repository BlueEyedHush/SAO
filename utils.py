def graph_to_networkx(graph):
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(graph.get_nodes())
    G.add_edges_from(graph.get_edges())
    return G


def strip_node(nodes):
    return map(lambda n: n.id, nodes)
