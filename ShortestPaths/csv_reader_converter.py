import csv
from datetime import datetime

from Graph import Graph


def read_connection_graph_file(file_name='connection_graph.csv'):
    connection_graph = []
    with open(file_name, 'r', encoding="utf8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            connection_graph.append(row)

    return connection_graph


def convert_connection_graph_to_graph(connection_graph, graph):
    for connection in connection_graph:
        graph.add_edge(connection['start_stop'],
                       connection['end_stop'],
                       connection['departure_time'],
                       connection['arrival_time'],
                       connection['line'],
                       connection['start_stop_lat'],
                       connection['start_stop_lon'],
                       connection['end_stop_lat'],
                       connection['end_stop_lon']
                       )


if __name__ == '__main__':
    proto_graph = read_connection_graph_file()
    graph = Graph()
    convert_connection_graph_to_graph(proto_graph, graph)
    print(graph)
