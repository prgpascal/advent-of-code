from math import inf
from utils.data_structures import Point

INFINITY = inf


def get_adjacent_positions(x: int, y: int, matrix) -> set[tuple[int, int]]:
    """"Given a list and a cell (expressed as "i" and "j" coordinates) returns the coordinates of all adjacent cells"""
    all_adjacent_positions = [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]
    return {
        point
        for point in all_adjacent_positions
        if point[0] in range(len(matrix)) and point[1] in range(len(matrix[0]))
    }


def sum_tuples(t1, t2):
    return tuple(sum(t) for t in zip(t1, t2))


def tuple_to_point(t) -> Point:
    x = y = z = 0
    if len(t) > 0:
        x = t[0]
    if len(t) > 1:
        y = t[1]
    if len(t) > 2:
        z = t[2]
    return Point(x, y, z)


def calculate_manhattan_distance(point_1: Point, point_2: Point):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])
