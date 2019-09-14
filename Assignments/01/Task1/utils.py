'''
Artificial Intelligence I
Assignment 1
Author: Bo Lin
Date of created: 09/09/2019
Date of modified: 09/10/2019
'''


class Node:

    def __init__(self, name):
        self.name = name
        self.inform = 0
        self.neighbors = dict()
        self.parent = None

    def get_all_neighbors(self):
        if len(self.neighbors.keys()) == 0:
            return None
        else:
            return self.neighbors.keys()

    def get_inform(self):
        return self.inform

    def get_neighbor_cost(self, neighbor_name):
        if neighbor_name not in self.neighbors.keys():
            return None
        else:
            return self.neighbors[neighbor_name]

    def add_neighbor(self, neighbor_name, neighbor_cost):
        self.neighbors[neighbor_name] = float(neighbor_cost)

    def set_inform(self, inform):
        self.inform = float(inform)

    def __lt__(self, other):
        return self.inform < other.inform


def get_input(input_args):
    graph_filename = input_args[1]
    origin_city = input_args[2]
    destination_city = input_args[3]
    is_informed = False
    if len(input_args) == 5:
        heuristic_filename = input_args[4]
        is_informed = True

    graph = _parsing_graph(graph_filename)
    if is_informed:
        graph = _parsing_heuristic(heuristic_filename, graph)
    if origin_city not in graph.keys() or destination_city not in graph.keys():
        raise ValueError(f"{origin_city} or {destination_city} not in graph")
    return graph, origin_city, destination_city


def _parsing_graph(graph_filename):
    graph = dict()
    with open(graph_filename, 'r') as f:
        content = f.read().splitlines()
    for each in content:
        if "END OF INPUT" in each:
            break
        city1_name, city2_name, value = each.strip().split(" ")
        try:
            city1_node = graph[city1_name]
        except KeyError:
            city1_node = Node(city1_name)
            graph[city1_name] = city1_node
        try:
            city2_node = graph[city2_name]
        except KeyError:
            city2_node = Node(city2_name)
            graph[city2_name] = city2_node
        city1_node.add_neighbor(city2_name, value)
        city2_node.add_neighbor(city1_name, value)
    return graph


def _parsing_heuristic(heuristic_filename, graph):
    with open(heuristic_filename, 'r') as f:
        content = f.read().splitlines()
    for each in content:
        if "END OF INPUT" in each:
            break
        city, value = each.strip().split(" ")
        graph[city].set_inform(value)
    return graph
