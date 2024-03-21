from dijsktra import *
from alternative_heuristics import alt_astar, alt_astar_transfers
from graph import Graph
from csv_reader_converter import convert_connection_graph_to_graph, read_connection_graph_file


def general_test_case(graph, criteria, start_stop, end_stop, start_time):
    start_time = time_to_seconds(start_time)
    alg_start_time = time.time()
    if criteria == 'dt':
        path, travel_time = dijkstra(graph, start_stop, end_stop, start_time)
    elif criteria == 'at':
        path, travel_time = astar(graph, start_stop, end_stop, start_time)
    elif criteria == 'p':
        path, number_of_transfers = astar_transfers(graph, start_stop, end_stop, start_time)
    elif criteria == 'alt':
        path, travel_time = alt_astar(graph, start_stop, end_stop, start_time)
    elif criteria == 'altp':
        path, number_of_transfers = alt_astar_transfers(graph, start_stop, end_stop, start_time)
    alg_end_time = time.time()

    if criteria == 'dt' or criteria == 'at' or criteria == 'alt':
        print(f"Travel time: {seconds_to_time(travel_time)}", file=sys.stderr, flush=True)
    elif criteria == 'p' or criteria == 'altp':
        print(f"Number of transfers: {number_of_transfers}", file=sys.stderr, flush=True)
    print(f"Run time: {alg_end_time - alg_start_time}", file=sys.stderr, flush=True)
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def dijkstra_test_cases(graph):
    general_test_case(graph, 'dt', 'Stanki', 'Lubelska', '11:00:00')
    general_test_case(graph, 'dt', 'Brzezia Łąka - Główna', 'Arkady (Capitol)', '11:15:00')
    general_test_case(graph, 'dt', 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego', '09:34:00')
    general_test_case(graph, 'dt', 'rondo Św. Ojca Pio', 'Sowia', '17:16:00')
    general_test_case(graph, 'dt', 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', '16:49:00')
    general_test_case(graph, 'dt', 'Tczewska', 'Park Wschodni', '14:32:00')
    general_test_case(graph, 'dt', 'Miękinia Cegielnia', 'Rdestowa', '09:09:00')


def astar_test_cases(graph):
    general_test_case(graph, 'at', 'Stanki', 'Lubelska', '11:00:00')
    general_test_case(graph, 'at', 'Brzezia Łąka - Główna', 'Arkady (Capitol)', '11:15:00')
    general_test_case(graph, 'at', 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego', '09:34:00')
    general_test_case(graph, 'at', 'rondo Św. Ojca Pio', 'Sowia', '17:16:00')
    general_test_case(graph, 'at', 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', '16:49:00')
    general_test_case(graph, 'at', 'Tczewska', 'Park Wschodni', '14:32:00')
    general_test_case(graph, 'at', 'Miękinia Cegielnia', 'Rdestowa', '09:09:00')


def transfers_test_cases(graph):
    general_test_case(graph, 'p', 'Iwiny - rondo', 'Hala Stulecia', '14:38:00')
    general_test_case(graph, 'p', 'Stanki', 'Lubelska', '11:00:00')
    general_test_case(graph, 'p', 'Brzezia Łąka - Główna', 'Arkady (Capitol)', '11:15:00')
    general_test_case(graph, 'p', 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego', '09:34:00')
    general_test_case(graph, 'p', 'rondo Św. Ojca Pio', 'Sowia', '17:16:00')
    general_test_case(graph, 'p', 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', '16:49:00')
    general_test_case(graph, 'p', 'Tczewska', 'Park Wschodni', '14:32:00')
    general_test_case(graph, 'p', 'Miękinia Cegielnia', 'Rdestowa', '09:09:00')


def time_transfers_comparison_test_cases(graph):
    print('Time variant')
    general_test_case(graph, 'at', 'Iwiny - rondo', 'Hala Stulecia', '14:38:00')
    print()

    print('Transfers variant')
    general_test_case(graph, 'p', 'Iwiny - rondo', 'Hala Stulecia', '14:38:00')

    print()
    print()
    print()

    print('Time variant')
    general_test_case(graph, 'at', 'Miękinia Cegielnia', 'Rdestowa', '14:16:00')
    print()

    print('Transfers variant')
    general_test_case(graph, 'p', 'Miękinia Cegielnia', 'Rdestowa', '14:16:00')

    print()
    print()
    print()

    print('Time variant')
    general_test_case(graph, 'at', 'Krucza', 'Inflancka', '15:05:00')
    print()

    print('Transfers variant')
    general_test_case(graph, 'p', 'Krucza', 'Inflancka', '15:05:00')


def alt_astar_test_cases(graph):
    general_test_case(graph, 'alt', 'Stanki', 'Lubelska', '11:00:00')
    general_test_case(graph, 'alt', 'Brzezia Łąka - Główna', 'Arkady (Capitol)', '11:15:00')
    general_test_case(graph, 'alt', 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego', '09:34:00')
    general_test_case(graph, 'alt', 'rondo Św. Ojca Pio', 'Sowia', '17:16:00')
    general_test_case(graph, 'alt', 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', '16:49:00')
    general_test_case(graph, 'alt', 'Tczewska', 'Park Wschodni', '14:32:00')
    general_test_case(graph, 'alt', 'Miękinia Cegielnia', 'Rdestowa', '09:09:00')


def alt_astar_transfers_test_cases(graph):
    general_test_case(graph, 'altp', 'Iwiny - rondo', 'Hala Stulecia', '14:38:00')
    general_test_case(graph, 'altp', 'Stanki', 'Lubelska', '11:00:00')
    general_test_case(graph, 'altp', 'Brzezia Łąka - Główna', 'Arkady (Capitol)', '11:15:00')
    general_test_case(graph, 'altp', 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego', '09:34:00')
    general_test_case(graph, 'altp', 'rondo Św. Ojca Pio', 'Sowia', '17:16:00')
    general_test_case(graph, 'altp', 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', '16:49:00')
    general_test_case(graph, 'altp', 'Tczewska', 'Park Wschodni', '14:32:00')
    general_test_case(graph, 'altp', 'Miękinia Cegielnia', 'Rdestowa', '09:09:00')


def average_number_of_connections_in_edges(graph):
    sum_of_connections = 0
    edges = 0
    for key in graph.get_nodes():
        for edge in graph.get_edges(key):
            edges += 1
            sum_of_connections += len(edge.connections)
    return sum_of_connections / edges


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    # print(average_number_of_connections_in_edges(stops_graph))

    # dijkstra_test_cases(stops_graph)

    print()
    print()
    print()

    # astar_test_cases(stops_graph)

    print()
    print()
    print()

    transfers_test_cases(stops_graph)

    print()
    print()
    print()

    time_transfers_comparison_test_cases(stops_graph)

    print()
    print()
    print()

    # alt_astar_test_cases(stops_graph)

    print()
    print()
    print()

    # alt_astar_transfers_test_cases(stops_graph)
