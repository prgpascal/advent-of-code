import os
from collections import defaultdict, deque
from utils.io import write_output
from utils.utils import INFINITY


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [list(line.strip()) for line in file]


def can_move_to_vertex(matrix, from_vertex, to_vertex):
    from_value = matrix[from_vertex[0]][from_vertex[1]]
    to_value = matrix[to_vertex[0]][to_vertex[1]]

    from_value = "a" if from_value == "S" else from_value
    from_value = "z" if from_value == "E" else from_value
    to_value = "a" if to_value == "S" else to_value
    to_value = "z" if to_value == "E" else to_value

    return ord(to_value) - ord(from_value) <= 1


def get_vertices_by_value(matrix, value):
    result = []
    for i, row in enumerate(matrix):
        result.extend([(i, j) for j, cell in enumerate(row) if cell == value])
    return result


def get_adjacent_vertices(from_vertex, matrix):
    adj = []
    if from_vertex[0] - 1 >= 0:
        adj.append((from_vertex[0] - 1, from_vertex[1]))
    if from_vertex[0] + 1 < len(matrix):
        adj.append((from_vertex[0] + 1, from_vertex[1]))
    if from_vertex[1] - 1 >= 0:
        adj.append((from_vertex[0], from_vertex[1] - 1))
    if from_vertex[1] + 1 < len(matrix[0]):
        adj.append((from_vertex[0], from_vertex[1] + 1))
    return adj


def create_graph(matrix):
    start_vertex = end_vertex = None
    edges = defaultdict(list)

    for i, _ in enumerate(matrix):
        for j, _ in enumerate(matrix[0]):
            vertex = (i, j)
            if matrix[i][j] == "E":
                end_vertex = vertex
            if matrix[i][j] == "S":
                start_vertex = vertex

            for adj in get_adjacent_vertices(vertex, matrix):
                if can_move_to_vertex(matrix, vertex, adj):
                    edges[vertex].append(adj)

    return (edges, start_vertex, end_vertex)


def bfs(edges, start_vertex, end_vertex):
    queue = deque()
    queue.append(start_vertex)
    distances = dict()
    distances[start_vertex] = 0

    while len(queue) > 0:
        item = queue.popleft()
        for adj in edges[item]:
            if adj not in distances:
                # unexplored vertex
                queue.append(adj)
                distances[adj] = distances[item] + 1

    return distances[end_vertex] if end_vertex in distances else INFINITY


def solve_1(input):
    edges, start_vertex, end_vertex = create_graph(input)
    return bfs(edges, start_vertex, end_vertex)


def solve_2(input):
    edges, start_vertex, end_vertex = create_graph(input)
    starting_vertices = [start_vertex]
    starting_vertices.extend(get_vertices_by_value(input, "a"))
    min_path = INFINITY
    for start in starting_vertices:
        min_path = min(min_path, bfs(edges, start, end_vertex))
    return min_path


input = read_input()
write_output(solve_1(input), solve_2(input))
