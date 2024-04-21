import math
import random
import copy

from dijsktra import *
from csv_reader_converter import *
from itertools import permutations


def modified_astar(graph, start_stop, end_stop, connection):
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
    shortest_distance[start_stop]['connection'] = connection

    while unseen_nodes:
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['cost'] + time_heuristic(end_stop, node))
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            weight_foot = infinity
            if min_node.name == child_node.end_stop.name and min_node.longitude != child_node.end_stop.longitude and min_node.latitude != child_node.end_stop.latitude:
                weight_foot = 60
                connection_foot = (shortest_distance[min_node]['connection'][1],
                                   shortest_distance[min_node]['connection'][1] + weight_foot, "Foot")

            connection, weight = get_closest_connection_and_weight(child_node.connections,
                                                                   shortest_distance[min_node]['connection'][1])

            if weight_foot < weight:
                weight = weight_foot
                connection = connection_foot

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

                return path

    if shortest_distance[end_stop]['cost'] == infinity:
        print("Path not reachable")
        return None

    current_node = end_stop
    while current_node != start_stop:
        path.insert(0, {'stop': current_node, 'connection': shortest_distance[current_node]['connection']})
        current_node = predecessor[current_node]['previous_stop']
    path.insert(0, {'stop': start_stop, 'connection': shortest_distance[start_stop]['connection']})

    return path


def mofified_astar_transfers(graph, start_stop, end_stop, connection):
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
    shortest_distance[start_stop]['connection'] = connection

    while unseen_nodes:
        min_node = min(unseen_nodes,
                       key=lambda node: shortest_distance[node]['transfers'] + transfer_heuristic(end_stop, node))
        unseen_nodes.pop(min_node)

        for child_node in graph.get_edges(min_node):
            next_connection = get_least_transfer_connection(child_node.connections,
                                                            shortest_distance[min_node]['connection'])

            if next_connection[2] == "Footpath":
                next_connection = (
                    shortest_distance[min_node]['connection'][1], shortest_distance[min_node]['connection'][1] + 60,
                    "Foot")

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


def calculate_time(path):
    time = 0
    for i in range(len(path) - 1):
        if path[i]['connection'][1] > path[i + 1]['connection'][1]:
            return sys.maxsize

    for i in range(len(path) - 1):
        time += path[i + 1]['connection'][1] - path[i]['connection'][1]

    return time


def calculate_number_of_transfers(path):
    number_of_transfers = 0
    for i in range(len(path) - 1):
        if path[i]['connection'][2] != path[i + 1]['connection'][2]:
            number_of_transfers += 1

    return number_of_transfers


def find_solution(graph, start_stop, required_stops, start_time):
    path = []
    last_stop = start_stop
    last_arrival_time = (0, start_time, "", False)

    path.append({'stop': start_stop, 'connection': (0, start_time, "", False)})

    for stop in required_stops:
        dijkstra_path = modified_astar(graph, last_stop, stop, last_arrival_time)

        path.extend(dijkstra_path[1:])
        last_stop = stop
        last_arrival_time = dijkstra_path[-1]['connection']

    dijkstra_path = modified_astar(graph, last_stop, start_stop, last_arrival_time)
    path.extend(dijkstra_path[1:])
    return path


def generate_neighbours(graph, current_solution, tabu_list, required_stops):
    neighbors = []

    for i in range(len(required_stops) - 1):
        for j in range(i + 1, len(required_stops)):
            new_required_stops = copy.deepcopy(required_stops)
            new_required_stops[i], new_required_stops[j] = new_required_stops[j], new_required_stops[i]

            if new_required_stops not in tabu_list:
                new_path = find_solution(graph, current_solution[0]['stop'], new_required_stops,
                                         current_solution[0]['connection'][1])
                neighbors.append(new_path)

    return neighbors


def tabu_search(graph, start_stop, required_stops_str, start_time):
    required_stops = required_stops_str.split(';')

    base_tabu_length = 5
    scaling_factor = 0.3
    min_tabu_length = 3
    max_tabu_length = 20

    dynamic_tabu_length = int(base_tabu_length + len(required_stops) * scaling_factor)
    tabu_list_size = max(min_tabu_length, min(max_tabu_length, dynamic_tabu_length))

    current_solution = find_solution(graph, start_stop, required_stops, start_time)
    best_solution = current_solution
    best_solution_fitness = calculate_time(current_solution)
    tabu_list = []

    max_iterations = 10

    for iteration in range(max_iterations):
        neighbors = generate_neighbours(graph, current_solution, tabu_list, required_stops)
        best_neighbor = None
        best_neighbor_fitness = float('inf')

        for neighbor in neighbors:
            neighbor_fitness = calculate_time(neighbor)
            if neighbor_fitness < best_neighbor_fitness and (
                    neighbor not in tabu_list or neighbor_fitness < best_solution_fitness):
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)
        tabu_list.append(best_neighbor)

        if calculate_time(best_neighbor) < calculate_time(best_solution):
            best_solution = best_neighbor
            best_solution_fitness = calculate_time(best_solution)

    return best_solution


def find_solution_transfers(graph, start_stop, required_stops, start_time):
    path = []
    last_stop = start_stop
    last_arrival_time = (0, start_time, "", False)

    path.append({'stop': start_stop, 'connection': (0, start_time, "", False)})

    for stop in required_stops:
        dijkstra_path = mofified_astar_transfers(graph, last_stop, stop, last_arrival_time)

        path.extend(dijkstra_path[0][1:])
        last_stop = stop
        last_arrival_time = dijkstra_path[0][-1]['connection']

    dijkstra_path = mofified_astar_transfers(graph, last_stop, start_stop, last_arrival_time)
    path.extend(dijkstra_path[0][1:])
    return path


def generate_neighbours_transfers(graph, current_solution, tabu_list, required_stops):
    neighbors = []

    for i in range(len(required_stops) - 1):
        for j in range(i + 1, len(required_stops)):
            new_required_stops = copy.deepcopy(required_stops)
            new_required_stops[i], new_required_stops[j] = new_required_stops[j], new_required_stops[i]

            if new_required_stops not in tabu_list:
                new_path = find_solution_transfers(graph, current_solution[0]['stop'], new_required_stops,
                                                   current_solution[0]['connection'][1])
                neighbors.append(new_path)

    return neighbors


def tabu_search_transfers(graph, start_stop, required_stops_str, start_time):
    required_stops = required_stops_str.split(';')

    base_tabu_length = 5
    scaling_factor = 0.3
    min_tabu_length = 3
    max_tabu_length = 20

    dynamic_tabu_length = int(base_tabu_length + len(required_stops) * scaling_factor)
    tabu_list_size = max(min_tabu_length, min(max_tabu_length, dynamic_tabu_length))

    current_solution = find_solution(graph, start_stop, required_stops, start_time)
    best_solution = current_solution
    best_solution_fitness = calculate_number_of_transfers(current_solution)
    tabu_list = []

    max_iterations = 10

    for iteration in range(max_iterations):
        neighbors = generate_neighbours_transfers(graph, current_solution, tabu_list, required_stops)
        best_neighbor = None
        best_neighbor_fitness = float('inf')

        for neighbor in neighbors:
            neighbor_fitness = calculate_number_of_transfers(neighbor)
            if neighbor_fitness < best_neighbor_fitness and (
                    neighbor not in tabu_list or neighbor_fitness < best_solution_fitness):
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        if len(tabu_list) >= tabu_list_size:
            tabu_list.pop(0)
        tabu_list.append(best_neighbor)

        if calculate_number_of_transfers(best_neighbor) < calculate_number_of_transfers(best_solution):
            best_solution = best_neighbor

    return best_solution


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    path = tabu_search(stops_graph, 'Zimowa', 'Ożynowa;Królewska;PL. STASZICA',
                       time_to_seconds('14:08:00'))

    print_path(path)
    print(calculate_time(path))

    print()
    print()
    print()

    required_stops = 'Ożynowa;Królewska;PL. STASZICA'.split(';')
    path = find_solution(stops_graph, 'Zimowa', required_stops, time_to_seconds('14:08:00'))
    print_path(path)
    print(calculate_time(path))
