import os
from utils.io import write_output
from collections import defaultdict


def read_input():
    edges = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            x, y = line.strip().split("-")
            edges.append((x, y))
    return edges


class Graph:
    def __init__(self):
        self.vertices = set()
        self.graph = defaultdict(list)

    def add_edge_and_vertices(self, start, end):
        self.vertices.add(start)
        self.vertices.add(end)
        self.graph[start].append(end)

    def do_path_contains_doubles(self, current_path):
        lower_path = [
            x for x in current_path if x.islower() and x != "start" and x != "end"
        ]
        lower_set = set(lower_path)
        return len(lower_path) != len(lower_set)

    def search_paths(self, v, visited, current_path, paths_found):
        if v.islower():
            visited[v] = True
        current_path.append(v)

        if v == "end":
            # End of path reached
            paths_found.append(current_path.copy())
        else:
            for i in self.graph[v]:
                if visited[i] is False:
                    self.search_paths(i, visited, current_path, paths_found)

        current_path.pop()
        visited[v] = False

    def search_paths_with_doubles(self, v, visited, current_path, paths_found):
        if v.islower():
            visited[v] = True
        current_path.append(v)

        if v == "end":
            # End of path reached
            paths_found.append(current_path.copy())
        else:
            for i in self.graph[v]:
                if i != "start":
                    if (visited[i] is False) or (
                        not self.do_path_contains_doubles(current_path)
                    ):
                        self.search_paths_with_doubles(
                            i, visited, current_path, paths_found
                        )

        current_path.pop()
        if v.islower():
            visited[v] = v in current_path


def create_graph():
    input = read_input()
    graph = Graph()
    for edge in input:
        graph.add_edge_and_vertices(edge[0], edge[1])
        graph.add_edge_and_vertices(edge[1], edge[0])
    return graph


def solve_1():
    graph = create_graph()
    visited = {v: False for v in graph.vertices}
    paths_found = []
    graph.search_paths("start", visited, [], paths_found)
    return len(paths_found)


def solve_2():
    graph = create_graph()
    visited = {v: False for v in graph.vertices}
    paths_found = []
    graph.search_paths_with_doubles("start", visited, [], paths_found)
    return len(paths_found)


write_output(solve_1(), solve_2())
