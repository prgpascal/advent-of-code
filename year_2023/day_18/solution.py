import os
import re
from dataclasses import dataclass
import sys
from utils.data_structures import Point
from utils.io import write_output
from utils.utils import calculate_polygon_area, hex_to_int

sys.setrecursionlimit(10000000)

DIRECTIONS = {"0": "R", "1": "D", "2": "L", "3": "U"}
MOVES = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}


@dataclass
class Step:
    direction: str
    steps: int
    color: str

    def from_hex_color(self):
        new_number = hex_to_int(self.color[1:-1])
        new_direction = DIRECTIONS[self.color[-1]]
        return Step(new_direction, new_number, self.color)


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            if match := re.search(r"([A-Z]) (\d+) \((.*)\)", line):
                direction, steps, color = match.groups()
                input.append(Step(direction, int(steps), color))
        return input


def visit_interior(position: Point, visited: set):
    if position not in visited:
        visited.add(position)
        for move in MOVES.values():
            visit_interior(Point(position.x + move[0], position.y + move[1]), visited)


def solve_1(input):
    position = Point(0, 0)
    visited = set()
    visited.add(position)
    for step in input:
        delta = MOVES[step.direction]
        for _ in range(step.steps):
            position = Point(position.x + delta[0], position.y + delta[1])
            visited.add(position)
    visit_interior(Point(1, 1), visited)
    return len(visited)


def compute_next_vertex(position, step):
    delta = MOVES[step.direction]
    return Point(position.x + delta[0] * step.steps, position.y + delta[1] * step.steps)


def solve_2(input):
    """Solved with the help of the Reddit community: https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kduw3z4"""
    input = [x.from_hex_color() for x in input]
    perimeter = 0
    vertices = []
    position = Point(0, 0)
    for step in input:
        next_vertex = compute_next_vertex(position, step)
        vertices.append(next_vertex)
        position = next_vertex
        perimeter += step.steps

    # Calculate the polygon area using the Shoelace formula
    polygon_area = calculate_polygon_area(vertices)

    # Get the number of internal points using the Pick's theorem
    interior_points = polygon_area - perimeter // 2 + 1
    return interior_points + perimeter


input = read_input()
write_output(solve_1(input), solve_2(input))
