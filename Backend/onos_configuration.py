import networkx as nx
import os

from Backend import data_format, bw_management
from Backend import best_path_algorithm as best_path
from Backend import read_iperfs as iperf_reader
from Backend import read_topology_csv
from Backend import json_generator
from Backend import request_sender

# Constants:
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = 'conf.json'


def configure_network(csv_file_path, iperf_file_path, ip, root_dir):
    # Initial network state
    global node1, node2, node_src_id
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

    # Json object to which all single flow jsons will be added
    conf_json = {'flows': []}
    global json_file_path
    json_file_path = f"{root_dir}\\{CONF_FILE}"

    # For each iperf stream
    for i in range(iperf_df.shape[0]):
            # Get node names by host ids from iperf
            node1_id = int(iperf_df.loc[i]['start'][1:])
            node2_id = int(iperf_df.loc[i]['c'][1:])
            for node in graph.nodes:
                if graph.nodes[node]['id'] == node1_id:
                    node1 = node
                if graph.nodes[node]['id'] == node2_id:
                    node2 = node
            # Find the best possible path between hosts mentioned in iperf
            path_data = best_path.find_best_path(graph, node1, node2)
            path = path_data[0]
            rtt = path_data[1]
            # Update bandwidths on the links of the shortest path
            bw_management.update_link_bandwidth(graph, path, iperf_df.loc[i:i], i, rtt)
            # Set up variables for JSON config creation
            if iperf_df.loc[i]['UDP'] == True:
                l4_type = 'udp'
            else:
                l4_type = 'tcp'
            dest_ip = f'10.0.0.{node2_id}'
            src_ip = f'10.0.0.{node1_id}'
            l4_port = iperf_df.loc[i]['p']

            # Generate switch to close host flow
            for node in graph.nodes:
                if node in path:
                    node_src_id = graph.nodes[node]['id']
                    self_host_ip = f"10.0.0.{node_src_id}"
                    host_flow = json_generator.generate_host_flow_json(node_src_id, 1, self_host_ip)
                    json_generator.add_entry_to_conf(host_flow, conf_json)

            # Generate Jsons for best path config - from client to server
            j = 0
            while path[j] != node2:
                for node in graph.nodes:
                    if node == path[j]:
                        node_src_id = graph.nodes[node]['id']
                node_src = path[j]
                node_dest = path[j + 1]
                j += 1
                out_port = int(data_format.get_port_data(network_data, node_src, node_dest)[0])

                single_json = json_generator.generate_single_json(node_src_id, out_port, dest_ip, l4_type, l4_port)
                json_generator.add_entry_to_conf(single_json, conf_json)

            # Generate Jsons for best path config - from server to client
            j = 0
            while list(reversed(path))[j] != node1:
                for node in graph.nodes:
                    if node == list(reversed(path))[j]:
                        node_src_id = graph.nodes[node]['id']
                node_src = list(reversed(path))[j]
                node_dest = list(reversed(path))[j + 1]
                j += 1
                out_port = int(data_format.get_port_data(network_data, node_src, node_dest)[0])

                single_json = json_generator.generate_single_return_json(node_src_id, out_port, src_ip, l4_type,
                                                                         l4_port)
                json_generator.add_entry_to_conf(single_json, conf_json)

            # Save all config to .json file
            json_generator.create_main_json_file(conf_json, json_file_path)


    # Send configuration file to ONOS
    request_sender.post_config(ip, json_file_path)

    return graph
