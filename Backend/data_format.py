import networkx as nx

from Backend import read_topology_csv as read_csv


def get_network_data_for_nx_graph(csv_data):
    # Getting network data from a .csv file
    conns = csv_data

    # Variable for a new formatted data to put in a NetworkX graph
    formatted_conns = []
    delay = 0
    bandwidth = 0
    for i in range(conns.shape[0]):
        formatted_conn = []
        for key in conns:
            if key == 'Node1':
                formatted_conn.append(conns.loc[i][key])
            elif key == 'Node2':
                formatted_conn.append(conns.loc[i][key])
            elif key == 'Delay':
                delay = conns.loc[i][key]
            elif key == 'Bandwidth':
                bandwidth = conns.loc[i][key]

        values = {'delay': delay, 'bandwidth': bandwidth}
        formatted_conn.append(values)
        formatted_conns.append(tuple(formatted_conn))

    return formatted_conns


def get_port_data(csv_data, node1, node2):
    # Getting network data from a .csv file
    conns = csv_data
    # Getting port numbers for a link with searched nodes

    searched_link = conns.loc[(conns['Node1'] == node1) & (conns['Node2'] == node2)].reset_index()
    searched_link_rev = conns.loc[(conns['Node1'] == node2) & (conns['Node2'] == node1)].reset_index()
    if not searched_link.empty:
        port_data = tuple([searched_link.loc[0]['Port1'], searched_link.loc[0]['Port2']])
    else:
        port_data = tuple(reversed([searched_link_rev.loc[0]['Port1'], searched_link_rev.loc[0]['Port2']]))

    return port_data


def set_switch_ids(graph):
    i = 1
    nodes = graph.nodes
    for node in nodes:
        attr = {f"{node}": {"id": i}}
        nx.set_node_attributes(graph, attr)
        i += 1

