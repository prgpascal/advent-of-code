from enum import Enum
from heapq import heappop, heappush
import os
from collections import defaultdict
from dataclasses import dataclass
from utils.data_structures import Point
from utils.io import write_output
from utils.utils import INFINITY


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
    direction_count: int

    def __lt__(self, other):
        return self.point < other.point


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        matrix = []
        for line in file:
            matrix.append([int(x) for x in list(line.strip())])
        return matrix


DIR_POINT = {Dir.U: (-1, 0), Dir.D: (1, 0), Dir.R: (0, 1), Dir.L: (0, -1)}
POINT_DIR = {(-1, 0): Dir.U, (1, 0): Dir.D, (0, 1): Dir.R, (0, -1): Dir.L}


def is_reversed_direction(direction_1: Dir, direction_2: Dir):
    x, y = DIR_POINT[direction_2]
    return DIR_POINT[direction_1] == (-x, -y)


def get_neighbors(vertex, matrix, ultra_crucibles):
    neighbors = []
    max_direction_count = 10 if ultra_crucibles else 3
    min_direction_count = 4 if ultra_crucibles else 0

    for (delta_x, delta_y), direction in POINT_DIR.items():
        x, y = vertex.point
        new_point = Point(x + delta_x, y + delta_y)

        if not valid_point(new_point, matrix):
            continue

        if is_reversed_direction(direction, vertex.direction):
            pass

        elif direction == vertex.direction:
            # continue same direction
            new_direction_count = vertex.direction_count + 1
            if new_direction_count <= max_direction_count:
                neighbors.append(Vertex(new_point, direction, new_direction_count))
        else:
            # change direction
            if vertex.direction_count >= min_direction_count:
                neighbors.append(Vertex(new_point, direction, 1))

    return neighbors


def valid_point(point, matrix):
    return 0 <= point.x < len(matrix) and 0 <= point.y < len(matrix[0])


def dijkstra(matrix, start, ultra_crucibles):
    start_vertex = Vertex(start, Dir.R, 0)
    dist = defaultdict(
        lambda: defaultdict(lambda: INFINITY)
    )  # point -> vertex -> heat_loss
    dist[start_vertex.point][start_vertex] = 0
    heap = [
        (0, start_vertex)
    ]  # (heat_loss, vertex). Use heat_loss just to optimize the priority queue
    while heap:
        _, vertex = heappop(heap)
        heat_loss = dist[vertex.point][vertex]
        for neighbor in get_neighbors(vertex, matrix, ultra_crucibles):
            x, y = neighbor.point
            new_heat_loss = heat_loss + matrix[x][y]
            if new_heat_loss < dist[neighbor.point][neighbor]:
                dist[neighbor.point][neighbor] = new_heat_loss
                heappush(heap, (new_heat_loss, neighbor))
    return dist


def solve_1(input):
    start = Point(0, 0)
    end = Point(len(input) - 1, len(input[0]) - 1)
    distances = dijkstra(input, start, False)
    return min(distances[end].values())


def solve_2(input):
    start = Point(0, 0)
    end = Point(len(input) - 1, len(input[0]) - 1)
    distances = dijkstra(input, start, True)
    return min(
        heat_loss
        for vertex, heat_loss in distances[end].items()
        if vertex.direction_count >= 4
    )


input = read_input()
write_output(solve_1(input), solve_2(input))
