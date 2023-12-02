import os
import re
from collections import Counter, deque, namedtuple, defaultdict
from dataclasses import dataclass
from functools import reduce
from utils.analysis import clock
from utils.data_structures import Point
from utils.io import create_matrix, write_output
from math import prod


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        # line by line
        for line in file:
            line = line.strip()

        # all lines
        return [line.strip() for line in file.readlines()]

    return input


def solve_1(input):
    return input


def solve_2(input):
    return "??"


input = read_input()
write_output(solve_1(input), solve_2(input))
