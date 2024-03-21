import math

from dijsktra import *
import sys


def calculate_number_of_connections(start_edges, end_edges):
    connections_from_start = 1
    connections_from_end = 1

    for start_edge in start_edges:
        connections_from_start += len(start_edge.connections)

    for end_edge in end_edges:
        connections_from_end += len(end_edge.connections)

    return connections_from_start + connections_from_end


def alt_time_heuristic(start_edges, end_edges):
    return (425 / calculate_number_of_connections(start_edges, end_edges)) * 300


def alt_transfers_heuristic(start_stop, end_stop):
    return math.ceil(425 / calculate_number_of_connections(start_stop, end_stop))


def alt_astar(graph, start_stop, end_stop, previous_arrival_time):
    shortest_distance = {}
    predecessor = {}
    unseen_nodes = graph.get_nodes().copy()
    infinity = sys.maxsize
    path = []
    start_stop = graph.get_vertex(start_stop)
    end_stop = graph.get_vertex(end_stop)

    for node in unseen_nodes:
        shortest_distance[node] = {
            'cost': infinity,
            'connection': (0, 0, "")
        }
    shortest_distance[start_stop]['cost'] = 0
    shortest_distance[start_stop]['connection'] = (0, previous_arrival_time, "")

    while unseen_nodes:
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['cost'] + alt_time_heuristic(graph.get_edges(start_stop), graph.get_edges(node)))
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            connection, weight = get_closest_connection(
                child_node.connections,
                shortest_distance[min_node]['connection'][1]
            )

            if weight + shortest_distance[min_node]['cost'] < shortest_distance[child_node.end_stop]['cost']:
                shortest_distance[child_node.end_stop]['cost'] = weight + shortest_distance[min_node]['cost']
                predecessor[child_node.end_stop] = {'previous_stop': min_node}
                shortest_distance[child_node.end_stop]['connection'] = connection

            if child_node.end_stop == end_stop:
                current_node = end_stop
                while current_node != start_stop:
                    path.insert(0, {'stop': current_node,
                                    'connection': shortest_distance[current_node]['connection']})
                    current_node = predecessor[current_node]['previous_stop']
                path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

                return path, shortest_distance[end_stop]['cost']

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['connection']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

    return path, shortest_distance[end_stop]['cost']


def alt_astar_transfers(graph, start_stop, end_stop, previous_arrival_time):
    shortest_distance = {}
    predecessor = {}
    unseen_nodes = graph.get_nodes().copy()
    infinity = sys.maxsize
    path = []
    start_stop = graph.get_vertex(start_stop)
    end_stop = graph.get_vertex(end_stop)

    for node in unseen_nodes:
        shortest_distance[node] = {
            'transfers': infinity,
            'connection': (0, 0, "")
        }
    shortest_distance[start_stop]['transfers'] = 0
    shortest_distance[start_stop]['connection'] = (0, previous_arrival_time, "")

    while unseen_nodes:
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['transfers'] + alt_transfers_heuristic(graph.get_edges(start_stop), graph.get_edges(end_stop)))
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            next_connection = get_least_transfer_connection(child_node.connections,
                                                            shortest_distance[min_node]['connection'])

            transfers = 1 if not next_connection[2] == shortest_distance[min_node]['connection'][2] else 0

            if transfers + shortest_distance[min_node]['transfers'] < shortest_distance[child_node.end_stop][
                'transfers']:
                shortest_distance[child_node.end_stop]['transfers'] = shortest_distance[min_node][
                                                                          'transfers'] + transfers
                predecessor[child_node.end_stop] = {'previous_stop': min_node}
                shortest_distance[child_node.end_stop]['connection'] = next_connection

            if child_node.end_stop == end_stop:
                current_node = end_stop
                while current_node != start_stop:
                    path.insert(0, {'stop': current_node,
                                    'connection': shortest_distance[current_node]['connection']})
                    current_node = predecessor[current_node]['previous_stop']
                path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

                return path, shortest_distance[end_stop]['transfers']

    if shortest_distance[end_stop]['transfers'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['connection']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

    return path, shortest_distance[end_stop]['transfers']


def testTime1(graph):
    print('For standard time heuristic')
    start_time = time.time()
    path, travel_time = astar(graph, 'Miękinia Cegielnia', 'Rdestowa', time_to_seconds('14:16:00'))
    end_time = time.time()

    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time)}\n")
    sys.stderr.write(f"Run time: {end_time - start_time}\n")
    print_path(path)

    print()
    print('For alternative time heuristic')
    start_time = time.time()
    path, travel_time = alt_astar(graph, 'Miękinia Cegielnia', 'Rdestowa',
                                  time_to_seconds('14:16:00'))
    end_time = time.time()

    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time)}\n")
    sys.stderr.write(f"Run time: {end_time - start_time}\n")
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testTime2(graph):
    print('For standard transfers heuristic')
    start_time = time.time()
    path, number_of_transfers = astar_transfers(graph, 'Krucza', 'Inflancka', time_to_seconds('15:05:00'))
    end_time = time.time()

    sys.stderr.write(f"Transfers: {number_of_transfers}\n")
    sys.stderr.write(f"Run time: {end_time - start_time}\n")
    print_path(path)

    print()
    print('For alternative transfers heuristic')
    start_time = time.time()
    path, number_of_transfers = alt_astar_transfers(graph, 'Krucza', 'Inflancka', time_to_seconds('15:05:00'))
    end_time = time.time()

    sys.stderr.write(f"Transfers: {number_of_transfers}\n")
    sys.stderr.write(f"Run time: {end_time - start_time}\n")
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    testTime1(stops_graph)

    testTime2(stops_graph)
