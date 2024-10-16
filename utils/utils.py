from math import inf
from utils.data_structures import Point
from math import gcd
import time

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


def sum_points(p1, p2):
    return Point(
        p1.x + p2.x,
        p1.y + p2.y,
        p1.z + p2.z,
    )


def tuple_to_point(t) -> Point:
    x = y = z = 0
    if len(t) > 0:
        x = t[0]
    if len(t) > 1:
        y = t[1]
    if len(t) > 2:
        z = t[2]
    return Point(x, y, z)


def hex_to_int(hex: str):
    return int(hex, 16)


def calculate_polygon_area(vertices: list[Point]):
    """Calculate the area of a polygon given its vertices (using the Shoelace formula)"""
    area = 0
    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i].x, vertices[i].y
        x2, y2 = vertices[i + 1].x, vertices[i + 1].y
        area += x1 * y2 - x2 * y1
    return abs(area) // 2


def calculate_manhattan_distance(point_1: Point, point_2: Point):
    """Calculate the manhattan distance between two points (2D plane)"""
    return abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y)


def calculate_lcm(numbers: list[int]):
    """Calculate the "least common multiple" of a list of numbers"""
    lcm = 1
    for n in numbers:
        lcm = lcm * n // gcd(lcm, n)
    return lcm


def hamming_distance(s1: str, s2: str):
    """Calculate the hamming distance between two strings with the same length"""
    assert len(s1) == len(s2)
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)


def get_current_time_millis():
    return round(time.time() * 1000)
