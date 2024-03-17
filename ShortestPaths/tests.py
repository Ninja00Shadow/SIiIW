from Dijsktra import *
from Graph import Graph
from csv_reader_converter import convert_connection_graph_to_graph, read_connection_graph_file


def testCase1(graph):
    path, travel_time = dijkstra(stops_graph, 'Stanki', 'Lubelska', time_to_seconds('11:00:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase2(graph):
    path, travel_time = astar(stops_graph, 'Brzezia Łąka - Główna', 'Arkady (Capitol)', time_to_seconds('11:15:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase3(graph):
    path, travel_time = dijkstra(stops_graph, 'Jerzmanowo (Cmentarz I)', 'pl. Daniłowskiego',
                                 time_to_seconds('09:34:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase4(graph):
    path, travel_time = dijkstra(stops_graph, 'rondo Św. Ojca Pio', 'Sowia', time_to_seconds('17:16:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase5(graph):
    path, travel_time = dijkstra(stops_graph, 'C.H. Aleja Bielany', 'Ślęza - skrzyżowanie', time_to_seconds('16:49:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase6(graph):
    path, travel_time = dijkstra(stops_graph, 'Tczewska', 'Park Wschodni', time_to_seconds('14:32:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase7(graph):
    path, travel_time = astar(stops_graph, 'Miękinia Cegielnia', 'Rdestowa', time_to_seconds('09:09:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def time_test_cases(graph):
    testCase1(graph)
    testCase2(graph)
    testCase3(graph)
    testCase4(graph)
    testCase5(graph)
    testCase6(graph)
    testCase7(graph)


def testCase101(graph):
    print('Time variant')
    path, travel_time = astar(stops_graph, 'Iwiny - rondo', 'Hala Stulecia', time_to_seconds('14:38:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print()
    print('Transfers variant')
    path, number_of_transfers = astar_transfers(stops_graph, 'Iwiny - rondo', 'Hala Stulecia',
                                                time_to_seconds('14:38:00'))

    print(number_of_transfers)
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase102(graph):
    print('Time variant')
    path, travel_time = astar(stops_graph, 'Miękinia Cegielnia', 'Rdestowa', time_to_seconds('14:16:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print()
    print('Transfers variant')
    path, number_of_transfers = astar_transfers(stops_graph, 'Miękinia Cegielnia', 'Rdestowa', time_to_seconds('14:16:00'))

    print(number_of_transfers)
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


def testCase103(graph):
    print('Time variant')
    path, travel_time = astar(stops_graph, 'Krucza', 'Inflancka', time_to_seconds('15:05:00'))

    print(seconds_to_time(travel_time))
    print_path(path)

    print()
    print('Transfers variant')
    path, number_of_transfers = astar_transfers(stops_graph, 'Krucza', 'Inflancka', time_to_seconds('15:05:00'))

    print(number_of_transfers)
    print_path(path)

    print('---------------------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    proto_graph = read_connection_graph_file('connection_graph2.csv')
    stops_graph = Graph()
    convert_connection_graph_to_graph(proto_graph, stops_graph)

    time_test_cases(stops_graph)

    print()
    print()
    print()

    testCase101(stops_graph)
    testCase102(stops_graph)
    testCase103(stops_graph)
