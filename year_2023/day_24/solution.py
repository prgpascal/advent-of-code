import os
import re
from collections import Counter, deque, namedtuple, defaultdict
from dataclasses import dataclass
from functools import reduce
from utils.analysis import clock
from utils.data_structures import Point
from utils.io import create_matrix, write_output
from math import prod
from itertools import combinations

from utils.utils import sum_points


def find_intersection(line_1_points, line_2_points):
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    p1_1, p1_2 = line_1_points
    p2_1, p2_2 = line_2_points
    x1, y1 = p1_1.x, p1_1.y
    x2, y2 = p1_2.x, p1_2.y
    x3, y3 = p2_1.x, p2_1.y
    x4, y4 = p2_2.x, p2_2.y
    try:
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        )
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        )
    except ZeroDivisionError:
        return None
    return Point(px, py)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            line = line.strip()
            position, velocity = line.split("@")
            x, y, z = [int(x.strip()) for x in position.split(",")]
            dx, dy, dz = [int(x.strip()) for x in velocity.split(",")]
            input.append((Point(x, y, z), Point(dx, dy, dz)))
    return input


def will_in_future(p1, v1, p2, v2, intersection):
    if (
        v1.x < 0
        and intersection.x > p1.x
        or v1.y < 0
        and intersection.y > p1.y
        or v2.x < 0
        and intersection.x > p2.x
        or v2.y < 0
        and intersection.y > p2.y
        or v1.x > 0
        and intersection.x < p1.x
        or v1.y > 0
        and intersection.y < p1.y
        or v2.x > 0
        and intersection.x < p2.x
        or v2.y > 0
        and intersection.y < p2.y
    ):
        return False
    return True


def slope(p1, p2):
    x1, y1, _ = p1
    x2, y2,_ = p2
    m = (y2-y1)/(x2-x1)
    return m

def in_test_area(intersect):
    TEST_AREA_MIN = 7
    TEST_AREA_MAX = 27
    # TEST_AREA_MIN = 200000000000000
    # TEST_AREA_MAX = 400000000000000
    if not intersect:
        return False
    x, y = intersect
    if (
        x >= TEST_AREA_MIN
        and x <= TEST_AREA_MAX
        and y >= TEST_AREA_MIN
        and y <= TEST_AREA_MAX
    ):
        return True
    return False


def solve_1(input):
    counter = 0
    for (p1, v1), (p2, v2) in combinations(input, 2):
        line_1_point_2 = sum_points(p1, v1)
        line_2_point_2 = sum_points(p2, v2)
        intersect = find_intersection((p1, line_1_point_2), (p2, line_2_point_2))
        if in_test_area(intersect) and will_in_future(p1, v1, p2, v2, intersect):
            counter += 1
    return counter


def solve_2(input):
    non_admitted_slopes = []
    for (p1, v1) in input:
        line_1_point_2 = sum_points(p1, v1)
        s = slope(line_1_point_2, p1)
        non_admitted_slopes.append(s)
    return sorted(non_admitted_slopes)


input = read_input()
write_output(solve_1(input), solve_2(input))
