from datetime import datetime


def time_to_seconds(time):
    hours = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    seconds2 = int(time.split(':')[2])
    return hours * 3600 + minutes * 60 + seconds2


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    seconds2 = seconds - hours * 3600 - minutes * 60
    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds2).zfill(2)}"


class Edge:
    def __init__(self, end_stop, arrival, departure, line):
        self.end_stop = end_stop
        self.departures_arrivals = [(time_to_seconds(departure), time_to_seconds(arrival), line)]

    def add_departure_arrival(self, departure, arrival, line):
        self.departures_arrivals.append((time_to_seconds(departure), time_to_seconds(arrival), line))

    def __str__(self):
        return f"End stop: {self.end_stop}, Departure and Arrivals: {self.departures_arrivals.__len__()}"

    def __repr__(self):
        return f"End stop: {self.end_stop}, Departure and Arrivals: {self.departures_arrivals.__len__()}"


class Vertex:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return f"Name: {self.name}, Longitude: {self.longitude}, Latitude: {self.latitude}"

    def __repr__(self):
        return f"Name: {self.name}, Longitude: {self.longitude}, Latitude: {self.latitude}"

    def __eq__(self, other):
        # return self.name == other.name and self.longitude == other.longitude and self.latitude == other.latitude
        return self.name == other.name

    def __hash__(self):
        return hash((self.longitude, self.latitude))
        # return hash(self.name)


class Graph:
    def __init__(self):
        self.graph = {}

    # def add_edge(self, start_stop, end_stop, departure, arrival, line, start_stop_lat,start_stop_lon,end_stop_lat,end_stop_lon):
    #     start_vertex = Vertex(start_stop,start_stop_lat,start_stop_lon)
    #     end_vertex = Vertex(end_stop,end_stop_lat,end_stop_lon)
    #
    #     if start_vertex not in self.graph:
    #         self.graph[start_vertex] = []
    #
    #     for edge in self.graph[start_vertex]:
    #         if edge.end_stop is not None and edge.end_stop == end_vertex:
    #             edge.add_departure_arrival(departure, arrival, line)
    #             return
    #
    #     self.graph[start_vertex].append(Edge(end_vertex, departure, arrival, line))
    #
    #     if end_vertex not in self.graph:
    #         self.graph[end_vertex] = []

    def add_edge(self, start_stop, end_stop, departure, arrival, line, start_stop_lat,start_stop_lon,end_stop_lat,end_stop_lon):
        # start_vertex = Vertex(start_stop,start_stop_lat,start_stop_lon)
        # end_vertex = Vertex(end_stop,end_stop_lat,end_stop_lon)

        if start_stop not in self.graph:
            self.graph[start_stop] = []

        for edge in self.graph[start_stop]:
            if edge.end_stop is not None and edge.end_stop == end_stop:
                edge.add_departure_arrival(departure, arrival, line)
                return

        self.graph[start_stop].append(Edge(end_stop, departure, arrival, line))

        if end_stop not in self.graph:
            self.graph[end_stop] = []

    def get_edges(self, start_stop):
        return self.graph[start_stop]

    def get_nodes(self):
        return self.graph

    # def get_vertex(self, name):
    #     return next((vertex for vertex in self.graph.keys() if vertex.name == name), None)

    # def copy_edge(self, start_stop, end_stop):
    #     for edge in self.graph[start_stop]:
    #         if edge.end_stop == end_stop:
    #             return start_stop, edge
    #
    # def add_edge_copy(self, start_stop, edge):
    #     self.graph[start_stop] = edge

    def __str__(self):
        return str(self.graph)

    def __repr__(self):
        return str(self.graph)

    def __eq__(self, other):
        return self.graph == other.stops_graph

    def __ne__(self, other):
        return self.graph != other.stops_graph

    def __hash__(self):
        return hash(self.graph)

    def __getitem__(self, key):
        return self.graph[key]

    def __setitem__(self, key, value):
        self.graph[key] = value

    def __delitem__(self, key):
        del self.graph[key]

    def __len__(self):
        return len(self.graph)

    def __iter__(self):
        return iter(self.graph)


if __name__ == '__main__':
    seconds = time_to_seconds("08:08:00")
    print(seconds)
    print(seconds_to_time(seconds))