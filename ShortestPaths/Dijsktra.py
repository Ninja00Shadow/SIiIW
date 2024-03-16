import math
import sys
import time
from heapq import heappush, heapify

from csv_reader_converter import *

from Graph import time_to_seconds, seconds_to_time


def shortest_time(items, pivot):
    # filtered_items = [item for item in items if item > pivot]
    filtered_items = [item for item in items if item >= pivot]  # TODO: check if it's correct
    if len(filtered_items) == 0:
        return ""
    return min(filtered_items, key=lambda x: abs(x - pivot))


def calculate_time_from_previous_arrival_to_next_arrival(previous_arrival_time, departures_arrivals):
    departures = [departure for departure, arrival, line in departures_arrivals]
    nearest_departure = shortest_time(departures, previous_arrival_time)
    if nearest_departure == "":
        return sys.maxsize
    return departures_arrivals[departures.index(nearest_departure)][1] - previous_arrival_time


def get_closest_connection(departures_arrivals, previous_arrival_time):
    departures = [departure for departure, arrival, line in departures_arrivals]
    nearest_departure = shortest_time(departures, previous_arrival_time)
    if nearest_departure == "":
        return (0, 0, "")
    return departures_arrivals[departures.index(nearest_departure)]


def calculate_euclides_distance(start_stop, end_stop):
    return math.dist([start_stop.longitude, end_stop.longitude], [start_stop.latitude, end_stop.latitude])


def is_line_in_connections(connections, line):
    for connection in connections:
        if connection[2] == line:
            return True
    return False


def print_path(path):
    sys.stdout.write(f"Starting point: {path[0]['stop']}, time: {seconds_to_time(path[0]['connection'][1])}\n")
    current_line = None
    odd = 1
    for i in range(1, len(path) - 1):
        if current_line is None:
            current_line = path[i]['connection'][2]
            sys.stdout.write(
                f"{path[i]['connection'][2]} | {path[i - 1]['stop']} {seconds_to_time(path[i]['connection'][0])} -> ")
            odd += 1
        elif current_line != path[i]['connection'][2]:
            sys.stdout.write(f"{path[i - 1]['stop']} {seconds_to_time(path[i - 1]['connection'][1])}\n")
            sys.stdout.write(
                f"{path[i]['connection'][2]} | {path[i - 1]['stop']} {seconds_to_time(path[i]['connection'][0])} -> ")
            current_line = path[i]['connection'][2]
            odd += 1

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
            'departure_arrival': (0, 0, "")
        }
    shortest_distance[start_stop]['cost'] = 0
    shortest_distance[start_stop]['departure_arrival'] = (0, previous_arrival_time, "")

    while unseen_nodes:
        min_node = min(unseen_nodes, key=lambda node: shortest_distance[node]['cost'])
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            weight = calculate_time_from_previous_arrival_to_next_arrival(
                shortest_distance[min_node]['departure_arrival'][1],
                child_node.departures_arrivals
            )

            if weight + shortest_distance[min_node]['cost'] < shortest_distance[child_node.end_stop]['cost']:
                shortest_distance[child_node.end_stop]['cost'] = weight + shortest_distance[min_node]['cost']
                predecessor[child_node.end_stop] = {'previous_stop': min_node}
                shortest_distance[child_node.end_stop]['departure_arrival'] = (
                    get_closest_connection(child_node.departures_arrivals,
                                           shortest_distance[min_node]['departure_arrival'][1])
                )

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['departure_arrival']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['departure_arrival']})

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
            'departure_arrival': (0, 0, "")
        }
    shortest_distance[start_stop]['cost'] = 0
    shortest_distance[start_stop]['departure_arrival'] = (0, previous_arrival_time, "")

    while unseen_nodes:
        # min_node = min(unseen_nodes, key=lambda node: calculate_euclides_distance(start_stop, node) + calculate_euclides_distance(end_stop, node))
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['cost'] + calculate_euclides_distance(end_stop, node))
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            weight = calculate_time_from_previous_arrival_to_next_arrival(
                shortest_distance[min_node]['departure_arrival'][1],
                child_node.departures_arrivals
            )

            if weight + shortest_distance[min_node]['cost'] < shortest_distance[child_node.end_stop]['cost']:
                shortest_distance[child_node.end_stop]['cost'] = weight + shortest_distance[min_node]['cost']
                predecessor[child_node.end_stop] = {'previous_stop': min_node}
                shortest_distance[child_node.end_stop]['departure_arrival'] = (
                    get_closest_connection(child_node.departures_arrivals,
                                           shortest_distance[min_node]['departure_arrival'][1])
                )

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['departure_arrival']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['departure_arrival']})

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
            'cost': infinity,
            'transfers': infinity,
            'departure_arrival': (0, 0, "")
        }
    shortest_distance[start_stop]['cost'] = 0
    shortest_distance[start_stop]['transfers'] = 0
    shortest_distance[start_stop]['departure_arrival'] = (0, previous_arrival_time, "")

    while unseen_nodes:
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['cost'] + shortest_distance[node][
                           'transfers'])  # Aktualizacja sposobu wyboru węzła
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            weight = calculate_time_from_previous_arrival_to_next_arrival(
                shortest_distance[min_node]['departure_arrival'][1],
                child_node.departures_arrivals
            )

            transfers = 1 if not is_line_in_connections(child_node.departures_arrivals,
                                                        shortest_distance[min_node]['departure_arrival'][2]) else 0

            cost = weight + shortest_distance[min_node]['cost'] + transfers * 60

            if cost < shortest_distance[child_node.end_stop]['cost']:
                shortest_distance[child_node.end_stop]['cost'] = cost
                shortest_distance[child_node.end_stop]['transfers'] = shortest_distance[min_node][
                                                                          'transfers'] + transfers
                predecessor[child_node.end_stop] = {'previous_stop': min_node}
                shortest_distance[child_node.end_stop]['departure_arrival'] = (
                    get_closest_connection(child_node.departures_arrivals,
                                           shortest_distance[min_node]['departure_arrival'][1])
                )

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['departure_arrival']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['departure_arrival']})

    return path, shortest_distance[end_stop]['cost']


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph_old.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    dijkstra_start_time = time.time()
    path, travel_time = dijkstra(stops_graph, 'Urząd Wojewódzki (Muzeum Narodowe)', 'Tramwajowa', time_to_seconds('5:00:00'))
    dijkstra_end_time = time.time()

    print_path(path)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time)}\n")
    sys.stderr.write(f"Run time: {dijkstra_end_time - dijkstra_start_time}\n")

    print("--------------------------------------------------------------------------------------------------")

    astar_start_time = time.time()
    path2, travel_time2 = astar(stops_graph, 'Stanki', 'Lubelska', time_to_seconds('11:00:00'))
    astar_end_time = time.time()

    print_path(path2)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time2)}\n")
    sys.stderr.write(f"Run time: {astar_end_time - astar_start_time}\n")

    print("--------------------------------------------------------------------------------------------------")

    astar_transfers_start_time = time.time()
    path3, travel_time3 = astar_transfers(stops_graph, 'Stanki', 'Lubelska', time_to_seconds('11:00:00'))
    astar_transfers_end_time = time.time()

    print_path(path3)
    sys.stderr.write(f"Travel time: {seconds_to_time(travel_time3)}\n")
    sys.stderr.write(f"Run time: {astar_transfers_end_time - astar_transfers_start_time}\n")
