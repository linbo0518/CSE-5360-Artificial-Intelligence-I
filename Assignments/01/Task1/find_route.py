'''
Artificial Intelligence I
Assignment 1
Author: Bo Lin
Date of created: 09/09/2019
Date of modified: 09/10/2019
'''

import sys
from utils import get_input
from search import Search

if __name__ == "__main__":
    graph, origin_city, destination_city = get_input(sys.argv)
    searcher = Search(graph)
    num_node_expanded, num_node_generate, max_node_in_memory, distance, node = searcher.search(
        origin_city, destination_city)

    output = ""
    if node is not None:
        route = [node.name]
        while node.parent is not None:
            route.append(node.parent.name)
            node = node.parent
        route = route[::-1]
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            output += "%s to %s, %.2f\n" % (start, end,
                                            graph[start].get_neighbor_cost(end))
    else:
        output = 'None\n'

    print("Nodes expanded: %d" % num_node_expanded)
    print("Nodes generated: %d" % num_node_generate)
    print("Max nodes in memory: %d" % max_node_in_memory)
    print("Distance: %.2f" % distance)
    print("Route:")
    print(output)
