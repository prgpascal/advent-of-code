import os
import re
from collections import Counter, deque, namedtuple, defaultdict
from dataclasses import dataclass
from functools import reduce
from utils.analysis import clock
from utils.data_structures import Point
from utils.io import create_matrix, write_output, print_matrix
from math import prod


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        matrix = [list(line.strip()) for line in file.readlines()]
        for i, row in enumerate(matrix):
            j = -1 if "S" not in row else row.index("S")
            if j >= 0:
                return (matrix, Point(i, j))


def get_neighbors(node: Point, matrix):
    DIRECTIONS = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    neighbors = []
    for dir in DIRECTIONS:
        new_point = Point(node.x + dir[0], node.y + dir[1])
        if new_point.x in range(len(matrix)) and new_point.y in range(len(matrix[0])):
            if matrix[new_point.x][new_point.y] != "#":
                neighbors.append(new_point)
    return neighbors


def solve_1(input):
    matrix, start_position = input
    N_STEPS = 26501365

    positions = set()
    positions.add(start_position)

    for _ in range(N_STEPS):
        new_positions = set()
        for p in positions:
            new_positions.update(get_neighbors(p, matrix))
        positions = new_positions
        
    return len(positions)


def solve_2(input):
    return "??"


input = read_input()
write_output(solve_1(input), solve_2(input))
