import read_topology_csv as read_csv


def get_network_data_for_nx_graph(file_path):
    # Getting network data from a .csv file
    conns = read_csv.read_topology(file_path)

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


def get_port_data(file_path, node1, node2):
    # Getting network data from a .csv file
    conns = read_csv.read_topology(file_path)

    # Getting port numbers for a link with searched nodes
    searched_link = conns.loc[(conns['Node1'] == node1) & (conns['Node2'] == node2)]
    port_data = tuple([searched_link.loc[0]['Port1'], searched_link.loc[0]['Port2']])

    return port_data


# print(get_network_data_for_nx_graph(r'C:\Users\EydaM\Desktop\Studia\Sem3\SCHT\LAB2\SCHT_ONOS_APP\resources\NetworkData.csv'))
# print(get_port_data(r'C:\Users\EydaM\Desktop\Studia\Sem3\SCHT\LAB2\SCHT_ONOS_APP\resources\NetworkData.csv', 'Londyn', 'Oslo'))