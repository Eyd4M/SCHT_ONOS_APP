import networkx as nx

from Backend import data_format, bw_management
from Backend import best_path_algorithm as best_path
from Backend import read_iperfs as iperf_reader
from Backend import read_topology_csv


def configure_network(csv_file_path, iperf_file_path):
    # Initial network state
    global node1, node2
    network_data = read_topology_csv.read_topology(csv_file_path)
    # Iperf file data
    iperf_df = iperf_reader.read_iperf(iperf_file_path)
    # Setup connections for a NetworkX graph
    conns = data_format.get_network_data_for_nx_graph(network_data)

    # Create empty graph
    graph = nx.Graph()
    # Adding connections between nodes - if a node doesn't exist NetworkX adds it in the process
    graph.add_edges_from(conns)
    # Assigning ids to switches - needed for correct packet destination ip address
    data_format.set_switch_ids(graph)

    # For each iperf stream
    for i in range(iperf_df.shape[0]):
        print(iperf_df.loc[i:i])
        # Get node names by host ids from iperf
        node1_id = int(iperf_df.loc[i]['start'][1:])
        node2_id = int(iperf_df.loc[i]['c'][1:])
        for node in graph.nodes:
            if graph.nodes[node]['id'] == node1_id:
                node1 = node
            if graph.nodes[node]['id'] == node2_id:
                node2 = node

        # Find the best possible path between hosts mentioned in iperf
        path_data = best_path.find_best_path(graph, node1, node2, iperf_df.loc[i:i], i)
        path = path_data[0]
        rtt = path_data[1]
        print(path)

        # Update bandwidths on the links of the shortest path
        bw_management.update_link_bandwidth(graph, path, iperf_df.loc[i:i], i, rtt)


    return graph






print(configure_network(r'C:\Users\EydaM\Desktop\Studia\Sem3\SCHT\LAB2\SCHT_ONOS_APP\resources\NetworkData.csv',r'C:\Users\EydaM\Desktop\Studia\Sem3\SCHT\LAB2\SCHT_ONOS_APP\resources\iperfs.txt').edges.data())