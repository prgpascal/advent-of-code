from enum import Enum
import os
from collections import deque, defaultdict
from dataclasses import dataclass
import sys
from utils.data_structures import Point
from utils.io import write_output
from utils.utils import get_current_time_millis

sys.setrecursionlimit(10000000)


class Dir(Enum):
    U = "UP"
    D = "DOWN"
    R = "RIGHT"
    L = "LEFT"
    X = "UNDEFINED"


@dataclass(unsafe_hash=True)
class Vertex:
    point: Point
    direction: Dir
    edges: list


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [list(line.strip()) for line in file.readlines()]


def get_neighbors(node, graph):
    max = len(graph)
    x, y = node.point
    neighbors = []
    if x - 1 >= 0 and graph[x - 1][y] in [".", "^"] and node.direction != Dir.D:
        neighbors.append(Vertex(Point(x - 1, y), Dir.U, []))
    if y + 1 < max and graph[x][y + 1] in [".", ">"] and node.direction != Dir.L:
        neighbors.append(Vertex(Point(x, y + 1), Dir.R, []))
    if y - 1 >= 0 and graph[x][y - 1] in [".", "<"] and node.direction != Dir.R:
        neighbors.append(Vertex(Point(x, y - 1), Dir.L, []))
    if x + 1 < max and graph[x + 1][y] in [".", "v"] and node.direction != Dir.U:
        neighbors.append(Vertex(Point(x + 1, y), Dir.D, []))
    return neighbors


def dfs_all_paths_lengths(graph, vertex, end_vertex, visited, path, paths):
    visited[vertex.point] = True
    path.append(vertex.point)

    if vertex.point == end_vertex.point:
        paths.append(len(path) - 1)
    else:
        for neighbor in get_neighbors(vertex, graph):
            if visited[neighbor.point] is False:
                dfs_all_paths_lengths(graph, neighbor, end_vertex, visited, path, paths)

    visited[vertex.point] = False
    path.pop()


def solve_1(input):
    start_point = Vertex(Point(0, input[0].index(".")), Dir.D, [])
    end_point = Vertex(Point(len(input) - 1, input[-1].index(".")), Dir.X, [])
    visited = defaultdict(lambda: False)
    result = []
    dfs_all_paths_lengths(input, start_point, end_point, visited, deque(), result)
    return max(result)


def get_neighbors_2(matrix, node: Point, visited: set):
    delta = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    neighbors = []
    for d in delta:
        possible_point = Point(node.x + d[0], node.y + d[1])
        if (
            possible_point.x >= 0
            and possible_point.x <= len(matrix) - 1
            and possible_point.y >= 0
            and possible_point.y <= len(matrix[0]) - 1
        ):
            if (
                matrix[possible_point.x][possible_point.y] == "."
                and possible_point not in visited
            ):
                neighbors.append(possible_point)
    return neighbors


def is_important_node(matrix, node):
    delta = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    neighbors = []
    for d in delta:
        possible_point = Point(node.x + d[0], node.y + d[1])
        if (
            possible_point.x >= 0
            and possible_point.x <= len(matrix) - 1
            and possible_point.y >= 0
            and possible_point.y <= len(matrix[0]) - 1
        ):
            if matrix[possible_point.x][possible_point.y] == ".":
                neighbors.append(possible_point)
    return len(neighbors) > 2


def create_min_graph(matrix, start_point, end_point):
    visited = set()
    graph = defaultdict(lambda: [])
    nodes_queue = deque()
    nodes_queue.append(start_point)
    while nodes_queue:
        node = nodes_queue.pop()
        visited.add(node)
        for neighbor in get_neighbors_2(matrix, node, visited):
            step_count = 1
            visited.add(neighbor)
            path_node = neighbor
            path_neigh = get_neighbors_2(matrix, path_node, visited)
            while len(path_neigh) == 1 and path_node != end_point:
                if is_important_node(matrix, path_node):
                    break
                step_count += 1
                path_node = path_neigh[0]
                path_neigh = get_neighbors_2(matrix, path_node, visited)
                visited.add(path_node)

            # found a new important node
            graph[node].append((path_node, step_count))
            graph[path_node].append((node, step_count))
            nodes_queue.append(path_node)
            visited.remove(path_node) # because we want to visit it again
    return graph


def dfs_graph(graph, vertex, end_point, visited, path, paths, time_last_max):
    point, weight = vertex
    visited[point] = True
    path.append(vertex)

    if get_current_time_millis() - time_last_max >= 5000:
        return

    if point == end_point:
        x = sum([x[1] for x in path])
        if x > paths[0]:
            paths[0] = x
            time_last_max = get_current_time_millis()

    else:
        for neighbor in graph[point]:
            if visited[neighbor[0]] is False:
                dfs_graph(
                    graph, neighbor, end_point, visited, path, paths, time_last_max
                )

    visited[point] = False
    path.pop()


def solve_2(input):
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] in [">", "^", "v", "<"]:
                input[i][j] = "."

    start_point = Point(0, input[0].index("."))
    end_point = Point(len(input) - 1, input[-1].index("."))
    graph = create_min_graph(input, start_point, end_point)

    visited = defaultdict(lambda: False)
    result = [0]

    for x in graph.values():
        x.sort(key=lambda x: -x[1])

    dfs_graph(
        graph,
        (start_point, 0),
        end_point,
        visited,
        deque(),
        result,
        get_current_time_millis(),
    )

    return max(result)


input = read_input()
write_output(solve_1(input), solve_2(input))
