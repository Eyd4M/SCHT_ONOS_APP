import networkx as nx
from matplotlib import pyplot as plt


def find_best_path(graph, node1, node2):

    # Dijkstra algorithm with our function (cost = default_bw/curr_bw based on SPF algorithm) for calculating weight
    path = nx.dijkstra_path(graph, node1, node2, weight=lambda u, v, d: (100 / d.get("bandwidth", 1) * d.get("delay", 1)))

    # Calculate RTT of the current path (for UDP criteria)
    rtt = 0
    delay = nx.get_edge_attributes(graph, 'delay')
    path_edges = list(zip(path, path[1:]))
    for edge in graph.edges():
        if edge in path_edges or tuple(reversed(edge)) in path_edges:
            rtt += delay[edge]
    rtt *= 2

    return path, rtt
