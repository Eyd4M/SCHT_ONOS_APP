import networkx as nx


def update_link_bandwidth(graph, path, single_iperf, iperf_number, rtt):

    # UDP stream
    if single_iperf.loc[iperf_number]['UDP']:
        pps = int(single_iperf.loc[iperf_number]['b'].replace('pps', ''))
        block_size = int(single_iperf.loc[iperf_number]['l'].replace('B', ''))
        # Calculating taken bandwidth considering an IP and UDP header size
        taken_bw = round(pps * (block_size+28) * 8 / 1000000, 2)
        print(taken_bw)

        path_edges = list(zip(path, path[1:]))
        for edge in graph.edges():
            if edge in path_edges or tuple(reversed(edge)) in path_edges:
                curr_bw = graph[edge[0]][edge[1]]['bandwidth']
                if curr_bw - taken_bw > 0:
                    graph[edge[0]][edge[1]]['bandwidth'] = round(curr_bw - taken_bw, 2)
                else:
                    graph[edge[0]][edge[1]]['bandwidth'] = 0.00000001
    # TCP stream
    else:
        drive_speed = int(single_iperf.loc[iperf_number]['b'].replace('m', ''))
        #data_size = int(single_iperf.loc[iperf_number]['n'].replace('M', ''))
        tcp_window = int(single_iperf.loc[iperf_number]['w'].replace('K', ''))
        taken_bw = min(round(((tcp_window * 8000) / (rtt/1000)) / 1000000, 2), drive_speed)
        print(taken_bw)

        path_edges = list(zip(path, path[1:]))
        for edge in graph.edges():
            if edge in path_edges or tuple(reversed(edge)) in path_edges:
                curr_bw = graph[edge[0]][edge[1]]['bandwidth']
                if curr_bw - taken_bw > 0:
                    graph[edge[0]][edge[1]]['bandwidth'] = round(curr_bw - taken_bw, 2)
                else:
                    graph[edge[0]][edge[1]]['bandwidth'] = 0.00000001

