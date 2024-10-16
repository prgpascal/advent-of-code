import os
from dataclasses import dataclass
from utils.data_structures import Point
from utils.io import write_output
from utils.utils import calculate_manhattan_distance


@dataclass(unsafe_hash=True)
class MutablePoint(Point):
    inc_x: int = 0  # increase on the X axis, due to expansion
    inc_y: int = 0  # increase on the Y axis, due to expansion


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [list(line.strip()) for line in file.readlines()]


def solve(input, expand_factor):
    empty_rows = set(list(range(len(input))))
    empty_columns = set(list(range(len(input))))
    points: set[MutablePoint] = set()
    counter = 1

    # find galaxies and empty rows/columns
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] != ".":
                # row i and column j are not empty
                empty_rows.discard(i)
                empty_columns.discard(j)
                points.add(MutablePoint(i, j))
                counter += 1

    # expand the universe by a scaling factor
    for point in points:
        for empty_x in empty_rows:
            if point.x > empty_x:
                point.inc_x += expand_factor
        for empty_y in empty_columns:
            if point.y > empty_y:
                point.inc_y += expand_factor

    # re-compute the position of all the points, based on the universe expansion
    for point in points:
        point.x += point.inc_x
        point.y += point.inc_y

    # calculate the Manhattan distance between all pairs of points
    pairs_of_points = [(p1, p2) for p1 in points for p2 in points if p1 != p2]
    all_distances = [calculate_manhattan_distance(p1, p2) for p1, p2 in pairs_of_points]

    return sum(all_distances) // 2  # divide by 2, because (p1, p2) == (p2, p1)


def solve_1(input):
    return solve(input, 1)


def solve_2(input):
    return solve(input, 999999)


input = read_input()
write_output(solve_1(input), solve_2(input))
