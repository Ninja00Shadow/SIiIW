import sys
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
        return previous_arrival_time
    return departures_arrivals[departures.index(nearest_departure)]


def dijkstra(graph, start_stop, end_stop, previous_arrival_time):
    shortest_distance = {}
    predecessor = {}
    unseen_nodes = graph.get_nodes().copy()
    infinity = sys.maxsize
    path = []
    # start_stop = graph.get_vertex(start_stop)
    # end_stop = graph.get_vertex(end_stop)

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
        path.insert(0, current_node)
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, start_stop)

    for stop in path:
        print(stop, end=" ")
        print(seconds_to_time(shortest_distance[stop]['departure_arrival'][0]), end=" ")
        print(seconds_to_time(shortest_distance[stop]['departure_arrival'][1]))

    print(f"Shortest path: {path}")
    print(f"Shortest distance: {shortest_distance[end_stop]['cost']}")
    return path


# def sub_graph(graph):
#     sub_graph = Graph()
#     start, edge = graph.copy_edge('PL. GRUNWALDZKI', 'Kliniki - Politechnika Wrocławska')
#     sub_graph.add_edge_copy(start, edge)
#     start, edge = graph.copy_edge('Kliniki - Politechnika Wrocławska', 'Hala Stulecia')
#     sub_graph.add_edge_copy(start, edge)
#     start, edge = graph.copy_edge('Hala Stulecia', 'Tramwajowa')
#     sub_graph.add_edge_copy(start, edge)
#     start, edge = graph.copy_edge('Tramwajowa', 'Chełmońskiego')
#     sub_graph.add_edge_copy(start, edge)


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    path = dijkstra(stops_graph, 'PL. GRUNWALDZKI', 'Chełmońskiego', time_to_seconds('08:08:00'))
    for stop in path[:-1]:
        for edge in stops_graph.get_edges(stop):
            if edge.end_stop == path[path.index(stop) + 1]:
                print(f"From {stop} to {edge.end_stop}")
                break
