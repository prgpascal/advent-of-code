import os
from heapq import heappop, heappush
from itertools import product
from utils.io import write_output


def read_input():
    matrix = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            matrix.append([int(x) for x in list(line.strip())])
    return matrix


def expand_matrix(matrix):
    # expand horizontally
    new_matrix = []
    for row in matrix:
        to_compute = new_row = row
        for _ in range(4):
            new_columns = [(x % 9) + 1 for x in to_compute]
            to_compute = new_columns
            new_row += new_columns
        new_matrix.append(new_row)

    # expand vertically
    to_compute = new_matrix.copy()
    for _ in range(4):
        matrix_section = to_compute
        to_compute = []
        for row in matrix_section:
            new_row = [(x % 9) + 1 for x in row]
            new_matrix.append(new_row)
            to_compute.append(new_row)

    return new_matrix


def get_neighbors(node, max):
    x, y = node
    neighbors = []
    if x - 1 >= 0:
        neighbors.append((x - 1, y))
    if y + 1 < max:
        neighbors.append((x, y + 1))
    if y - 1 >= 0:
        neighbors.append((x, y - 1))
    if x + 1 < max:
        neighbors.append((x + 1, y))
    return neighbors


def dijkstra(graph, source, target):
    n = len(graph)
    visited = {(x, y): False for (x, y) in product(range(n), repeat=2)}
    dist = {(x, y): float("inf") for (x, y) in product(range(n), repeat=2)}
    dist[source] = graph[source[0]][source[1]]
    heap = [(0, source)]
    while heap:
        dist_node, node = heappop(heap)
        if not visited[node]:
            visited[node] = True
            if node == target:
                break
            for neighbor in get_neighbors(node, n):
                x, y = neighbor
                dist_neighbor = dist_node + graph[x][y]
                if dist_neighbor < dist[neighbor]:
                    dist[neighbor] = dist_neighbor
                    heappush(heap, (dist_neighbor, neighbor))
    return dist[target]


def solve_1():
    input = read_input()
    return dijkstra(input, (0, 0), (len(input) - 1, len(input) - 1))


def solve_2():
    input = expand_matrix(read_input())
    return dijkstra(input, (0, 0), (len(input) - 1, len(input) - 1))


write_output(solve_1(), solve_2())
