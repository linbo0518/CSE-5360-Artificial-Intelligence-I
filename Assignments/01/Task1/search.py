'''
Artificial Intelligence I
Assignment 1
Author: Bo Lin
Date of created: 09/09/2019
Date of modified: 09/10/2019
'''
from queue import PriorityQueue
from utils import Node


class Search:

    def __init__(self, graph):
        self.num_node_expanded = 0
        self.num_node_generate = 0
        self.max_node_in_memory = 0
        self.fringe = PriorityQueue()
        self.closed = list()
        self.graph = graph
        self.optimal_num_node_expanded = 0
        self.optimal_num_node_generate = 0
        self.optimal_max_node_in_memory = 0
        self.optimal_node = None
        self.optimal_distance = float('inf')

    def search(self, origin_city, destination_city):
        self.fringe.put(
            (0 + self.graph[origin_city].get_inform(), Node(origin_city)))
        self.max_node_in_memory = 1

        while self.fringe.qsize() > 0:
            cur_cost, cur_node = self.expand_node()
            if cur_node.name == destination_city:
                distance = cur_cost - self.graph[cur_node.name].get_inform()
                if distance < self.optimal_distance:
                    self.optimal_node = cur_node
                    self.optimal_distance = distance
                    self.optimal_num_node_expanded = self.num_node_expanded
                    self.optimal_num_node_generate = self.num_node_generate
                    self.optimal_max_node_in_memory = self.max_node_in_memory
            self.generate_node(cur_cost, cur_node)
            self.update_max_node_in_memory()
            self.closed.append(cur_node.name)
        if self.optimal_node is None:
            self.optimal_num_node_expanded = self.num_node_expanded
            self.optimal_num_node_generate = self.num_node_generate
            self.optimal_max_node_in_memory = self.max_node_in_memory
        return self.optimal_num_node_expanded, self.optimal_num_node_generate, \
            self.optimal_max_node_in_memory, self.optimal_distance, self.optimal_node

    def expand_node(self):
        cost, node = self.fringe.get()
        self.num_node_expanded += 1
        return cost, node

    def generate_node(self, cur_cost, cur_node):
        cur_ref_node = self.graph[cur_node.name]
        if cur_node.name not in self.closed:
            neighbors = cur_ref_node.get_all_neighbors()
            for each_name in neighbors:
                node = Node(each_name)
                node.parent = cur_node
                self.fringe.put(
                    (cur_cost + cur_ref_node.get_neighbor_cost(each_name) -
                     cur_ref_node.get_inform() +
                     self.graph[each_name].get_inform(), node))
            self.num_node_generate += len(neighbors)

    def update_max_node_in_memory(self):
        if self.max_node_in_memory < self.fringe.qsize():
            self.max_node_in_memory = self.fringe.qsize()

    def __repr__(self):
        output = "Nodes expanded: " + str(self.num_node_expanded) + "\n"
        output += "Nodes generated: " + str(self.num_node_generate) + "\n"
        output += "Max nodes in memory: " + str(self.max_node_in_memory) + "\n"
        output += "Closed: " + str(set(self.closed)) + "\n"
        return output