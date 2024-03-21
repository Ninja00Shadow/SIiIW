import math
import sys
import time
from math import sin, cos, sqrt, atan2, radians

from csv_reader_converter import *

from graph import time_to_seconds, seconds_to_time


def shortest_time(connections, pivot):
    filtered_items = [item for item in connections if item >= pivot]
    if len(filtered_items) == 0:
        return min(connections)
    return min(filtered_items, key=lambda x: abs(x - pivot))


# def calculate_time_from_previous_arrival_to_next_arrival(previous_arrival_time, connections):
#     departures = [departure for departure, arrival, line, night in connections]
#     nearest_departure = shortest_time(departures, previous_arrival_time)
#     if nearest_departure < previous_arrival_time:
#         return connections[departures.index(nearest_departure)][1] + 84600 - previous_arrival_time
#     return connections[departures.index(nearest_departure)][1] - previous_arrival_time


def get_closest_connection(connections, previous_arrival_time):
    departures = [departure for departure, arrival, line, night in connections]
    nearest_departure = shortest_time(departures, previous_arrival_time)
    if nearest_departure == "":
        return (0, 0, "")

    if nearest_departure < previous_arrival_time:
        return connections[departures.index(nearest_departure)], connections[departures.index(nearest_departure)][1] + 84600 - previous_arrival_time
    return connections[departures.index(nearest_departure)], connections[departures.index(nearest_departure)][1] - previous_arrival_time


def calculate_distance(start_stop, end_stop):
    R = 6373.0

    lat1 = radians(start_stop.latitude)
    lon1 = radians(start_stop.longitude)
    lat2 = radians(end_stop.latitude)
    lon2 = radians(end_stop.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000


def time_heuristic(start_stop, end_stop):
    return calculate_distance(start_stop, end_stop) / 5


def transfer_heuristic(start_stop, end_stop):
    return math.ceil(calculate_distance(start_stop, end_stop) / 3000)


def get_least_transfer_connection(connections, previous_line):
    if previous_line[2] == "":
        connection, weight = get_closest_connection(connections, previous_line[1])
        return connection

    filtered_connections = [connection for connection in connections if connection[0] >= previous_line[1]]
    if len(filtered_connections) == 0:
        filtered_connections = [connection for connection in connections if connection[0] < previous_line[1]]

    filtered_connections = sorted(filtered_connections, key=lambda x: x[0])

    for connection in filtered_connections:
        if connection[2] == previous_line[2]:
            return connection

    connection, weight = get_closest_connection(connections, previous_line[1])
    return connection


def print_path(path):
    sys.stdout.write(f"Starting point: {path[0]['stop']}, time: {seconds_to_time(path[0]['connection'][1])}\n")
    current_line = None
    for i in range(1, len(path)):
        if current_line is None:
            current_line = path[i]['connection'][2]
            sys.stdout.write(
                f"{path[i]['connection'][2]} | {path[i - 1]['stop']} {seconds_to_time(path[i]['connection'][0])} -> ")
        elif current_line != path[i]['connection'][2]:
            sys.stdout.write(f"{path[i - 1]['stop']} {seconds_to_time(path[i - 1]['connection'][1])}\n")
            sys.stdout.write(
                f"{path[i]['connection'][2]} | {path[i - 1]['stop']} {seconds_to_time(path[i]['connection'][0])} -> ")
            current_line = path[i]['connection'][2]

    sys.stdout.write(f"{path[-1]['stop']} {seconds_to_time(path[-1]['connection'][1])}\n")
    sys.stdout.write(f"Destination: {path[-1]['stop']}, time: {seconds_to_time(path[-1]['connection'][1])}\n")


def dijkstra(graph, start_stop, end_stop, previous_arrival_time):
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
        min_node = min(unseen_nodes, key=lambda node: shortest_distance[node]['cost'])
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

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['connection']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

    return path, shortest_distance[end_stop]['cost']


def astar(graph, start_stop, end_stop, previous_arrival_time):
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
                       key=lambda node: shortest_distance[node]['cost'] + time_heuristic(end_stop, node))
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


def astar_transfers(graph, start_stop, end_stop, previous_arrival_time):
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
                       key=lambda node: shortest_distance[node]['transfers'] + transfer_heuristic(end_stop, node))
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


def cli():
    print("Starting point: ")
    start_stop = input()
    print("Destination: ")
    end_stop = input()
    print("Criteria: (t) time, (p) transfers ")
    criteria = input()
    print("Time: ")
    time = input()

    start_time = time.time()
    if criteria == 't':
        path, travel_time = dijkstra(stops_graph, start_stop, end_stop, time_to_seconds(time))
    elif criteria == 'p':
        path, number_of_transfers = astar_transfers(stops_graph, start_stop, end_stop, time_to_seconds(time))
    end_time = time.time()

    print_path(path)
    if criteria == 't':
        sys.stderr.write(f"Travel time: {seconds_to_time(travel_time)}\n")
    elif criteria == 'p':
        sys.stderr.write(f"Number of transfers: {number_of_transfers}\n")
    sys.stderr.write(f"Run time: {end_time - start_time}\n")


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    dijkstra_start_time = time.time()
    path, travel_time = dijkstra(stops_graph, 'Iwiny - rondo', 'Hala Stulecia', time_to_seconds('14:38:00'))
    dijkstra_end_time = time.time()

    print_path(path)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time)}\n")
    sys.stderr.write(f"Run time: {dijkstra_end_time - dijkstra_start_time}\n")

    print("--------------------------------------------------------------------------------------------------")

    astar_start_time = time.time()
    path2, travel_time2 = astar(stops_graph, 'Iwiny - rondo', 'Hala Stulecia', time_to_seconds('14:38:00'))
    astar_end_time = time.time()

    print_path(path2)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time2)}\n")
    sys.stderr.write(f"Run time: {astar_end_time - astar_start_time}\n")

    print("--------------------------------------------------------------------------------------------------")

    astar_transfers_start_time = time.time()
    path3, travel_time3 = astar_transfers(stops_graph, 'Iwiny - rondo', 'Hala Stulecia', time_to_seconds('14:38:00'))
    astar_transfers_end_time = time.time()

    print_path(path3)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time3)}\n")
    sys.stderr.write(f"Run time: {astar_transfers_end_time - astar_transfers_start_time}\n")
