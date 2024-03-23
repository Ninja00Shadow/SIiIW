from datetime import datetime


def time_to_seconds(time):
    hours, minutes, seconds = [int(part) for part in time.split(':')]
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    seconds2 = seconds - hours * 3600 - minutes * 60
    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds2).zfill(2)}"


class Edge:
    def __init__(self, end_stop, arrival, departure, line):
        self.end_stop = end_stop
        arrival = time_to_seconds(arrival)
        departure = time_to_seconds(departure)
        night = True if departure > 86400 or arrival > 86400 else False
        if night:
            arrival = arrival - 86400
            departure = departure - 86400
        self.connections = [(departure, arrival, line, night)]

    def add_connection(self, departure, arrival, line):
        arrival = time_to_seconds(arrival)
        departure = time_to_seconds(departure)
        night = True if departure > 86400 or arrival > 86400 else False
        if night:
            arrival = arrival - 86400
            departure = departure - 86400
        self.connections.append((departure, arrival, line, night))

    def __str__(self):
        return f"End stop: {self.end_stop}, Departure and Arrivals: {self.connections.__len__()}"

    def __repr__(self):
        return f"End stop: {self.end_stop}, Departure and Arrivals: {self.connections.__len__()}"


class Vertex:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if type(other) is str:
            return self.name == other
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start_stop, end_stop, departure, arrival, line, start_stop_lat, start_stop_lon, end_stop_lat,
                 end_stop_lon):
        start_vertex = Vertex(start_stop, start_stop_lat, start_stop_lon)
        end_vertex = Vertex(end_stop, end_stop_lat, end_stop_lon)

        if start_vertex not in self.graph:
            self.graph[start_vertex] = []

        for edge in self.graph[start_vertex]:
            if edge.end_stop is not None and edge.end_stop == end_vertex:
                edge.add_connection(departure, arrival, line)
                return

        self.graph[start_vertex].append(Edge(end_vertex, departure, arrival, line))

        if end_vertex not in self.graph:
            self.graph[end_vertex] = []

    def get_edges(self, start_stop):
        return self.graph[start_stop]

    def get_nodes(self):
        return self.graph

    def get_vertex(self, name):
        return next((vertex for vertex in self.graph.keys() if vertex.name == name), None)

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
