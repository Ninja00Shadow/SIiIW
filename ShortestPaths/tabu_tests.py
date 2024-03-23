import time

from csv_reader_converter import read_connection_graph_file, convert_connection_graph_to_graph
from dijsktra import print_path
from graph import time_to_seconds, Graph, seconds_to_time
from tabu_search import calculate_time, tabu_search, find_solution, tabu_search_transfers, \
    calculate_number_of_transfers, find_solution_transfers


def general_test_case(graph, criteria, start_stop, required_stops, arrival_time):
    if criteria == 't':
        print("Time version")
        alg_start_time = time.time()
        print("Tabu search solution:")
        path = tabu_search(graph, start_stop, required_stops, time_to_seconds(arrival_time))
        alg_end_time = time.time()
        print(f"Run time: {alg_end_time - alg_start_time}")
        print_path(path)
        print("Total travel time: ", seconds_to_time(calculate_time(path)))

        print()
        print()

        required_stops = required_stops.split(';')
        path = find_solution(graph, start_stop, required_stops, time_to_seconds(arrival_time))
        print("A* solution:")
        print_path(path)
        print("Total travel time: ", seconds_to_time(calculate_time(path)))

        print('---------------------------------------------------------------------------------------------------------')

    elif criteria == 'p':
        print("Transfers version")
        alg_start_time = time.time()
        print("Tabu search solution:")
        path = tabu_search_transfers(graph, start_stop, required_stops, time_to_seconds(arrival_time))
        alg_end_time = time.time()
        print(f"Run time: {alg_end_time - alg_start_time}")
        print_path(path)
        print("Total number of transfers: ", calculate_number_of_transfers(path))

        print()
        print()

        required_stops = required_stops.split(';')
        path = find_solution_transfers(graph, start_stop, required_stops, time_to_seconds(arrival_time))
        print("A* solution:")
        print_path(path)
        print("Total number of transfers: ", calculate_number_of_transfers(path))

        print('---------------------------------------------------------------------------------------------------------')


def tabu_tests_time(graph):
    general_test_case(graph, 't', 'Zimowa', 'Ożynowa;Królewska;PL. STASZICA','14:08:00')

    general_test_case(graph, 't', 'Fiołkowa', 'Kwidzyńska;Sztabowa;Złotostocka;DWORZEC GŁÓWNY','12:36:00')


def tabu_tests_transfers(graph):
    general_test_case(graph, 'p', 'Zimowa', 'Ożynowa;Królewska;PL. STASZICA','14:08:00')

    general_test_case(graph, 'p', 'Fiołkowa', 'Kwidzyńska;Sztabowa;Złotostocka;DWORZEC GŁÓWNY','12:36:00')


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    tabu_tests_time(stops_graph)

    # tabu_tests_transfers(stops_graph)
