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

    # path_edges = list(zip(path, path[1:]))
    #
    # # Create a list of all edges, and assign colors based on whether they are in the shortest path or not
    # edge_colors = [
    #     "red" if edge in path_edges or tuple(reversed(edge)) in path_edges else "black"
    #     for edge in graph.edges()
    # ]
    #
    # # Visualize the graph
    # pos = nx.spring_layout(graph)
    # nx.draw_networkx_nodes(graph, pos)
    # nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    # nx.draw_networkx_labels(graph, pos)
    # nx.draw_networkx_edge_labels(
    #    graph, pos, edge_labels={(u, v): d["bandwidth"] for u, v, d in graph.edges(data=True)}
    # )
    #
    # plt.show()
    return path, rtt
