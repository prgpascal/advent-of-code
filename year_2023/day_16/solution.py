import os
import sys
from utils.analysis import clock
from utils.data_structures import Point
from utils.io import write_output

sys.setrecursionlimit(10000)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [list(line.strip()) for line in file.readlines()]


def point_in_matrix(matrix, point: Point) -> bool:
    return (
        point.x >= 0
        and point.x < len(matrix)
        and point.y >= 0
        and point.y < len(matrix[0])
    )


def navigate(
    matrix: list[list[str]],
    point: Point,
    direction: str,
    visited: set[tuple[Point, str]],
):
    if (point, direction) in visited:
        return

    visited.add((point, direction))
    this_point = matrix[point.x][point.y]
    next_points = []

    if this_point == "." and direction == "R":
        next_points.append((Point(point.x, point.y + 1), direction))
    elif this_point == "." and direction == "L":
        next_points.append((Point(point.x, point.y - 1), direction))
    elif this_point == "." and direction == "T":
        next_points.append((Point(point.x - 1, point.y), direction))
    elif this_point == "." and direction == "B":
        next_points.append((Point(point.x + 1, point.y), direction))

    elif this_point == "|" and direction in ("R", "L"):
        next_points.append((Point(point.x - 1, point.y), "T"))
        next_points.append((Point(point.x + 1, point.y), "B"))
    elif this_point == "|" and direction in ("T"):
        next_points.append((Point(point.x - 1, point.y), direction))
    elif this_point == "|" and direction in ("B"):
        next_points.append((Point(point.x + 1, point.y), direction))

    elif this_point == "-" and direction in ("T", "B"):
        next_points.append((Point(point.x, point.y - 1), "L"))
        next_points.append((Point(point.x, point.y + 1), "R"))
    elif this_point == "-" and direction in ("R"):
        next_points.append((Point(point.x, point.y + 1), direction))
    elif this_point == "-" and direction in ("L"):
        next_points.append((Point(point.x, point.y - 1), direction))

    elif this_point == "/" and direction in ("R"):
        next_points.append((Point(point.x - 1, point.y), "T"))
    elif this_point == "/" and direction in ("L"):
        next_points.append((Point(point.x + 1, point.y), "B"))
    elif this_point == "/" and direction in ("T"):
        next_points.append((Point(point.x, point.y + 1), "R"))
    elif this_point == "/" and direction in ("B"):
        next_points.append((Point(point.x, point.y - 1), "L"))

    elif this_point == "\\" and direction in ("R"):
        next_points.append((Point(point.x + 1, point.y), "B"))
    elif this_point == "\\" and direction in ("L"):
        next_points.append((Point(point.x - 1, point.y), "T"))
    elif this_point == "\\" and direction in ("T"):
        next_points.append((Point(point.x, point.y - 1), "L"))
    elif this_point == "\\" and direction in ("B"):
        next_points.append((Point(point.x, point.y + 1), "R"))

    for point, direction in next_points:
        if point_in_matrix(matrix, point):
            navigate(matrix, point, direction, visited)


def solve_1(input):
    visited = set()
    navigate(input, Point(0, 0), "R", visited)
    return len(set(point[0] for point in visited))


def solve_2(input):
    max_visited = 0
    starting_points = []

    # corners
    starting_points.append((Point(0, 0), "R"))
    starting_points.append((Point(0, 0), "B"))
    starting_points.append((Point(0, len(input[0]) - 1), "L"))
    starting_points.append((Point(0, len(input[0]) - 1), "B"))
    starting_points.append((Point(len(input) - 1, 0), "T"))
    starting_points.append((Point(len(input) - 1, 0), "R"))
    starting_points.append((Point(len(input) - 1, len(input[0]) - 1), "T"))
    starting_points.append((Point(len(input) - 1, len(input[0]) - 1), "L"))

    # edges
    for j in range(1, len(input[0]) - 1):
        starting_points.append((Point(0, j), "B"))
        starting_points.append((Point(len(input) - 1, j), "T"))
    for i in range(1, len(input) - 1):
        starting_points.append((Point(i, 0), "R"))
        starting_points.append((Point(i, len(input[0]) - 1), "L"))

    for point, direction in starting_points:
        visited = set()
        navigate(input, point, direction, visited)
        max_visited = max(max_visited, len(set(point[0] for point in visited)))
    return max_visited


input = read_input()
write_output(solve_1(input), solve_2(input))
