import os
from utils.io import write_output
from collections import deque, Counter


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        # line by line
        for line in file:
            line = line.strip()

        # all lines
        input = [line.strip() for line in file.readlines()]

    return input


def solve_1(input):
    return input


def solve_2(input):
    return input


input = read_input()
write_output(os.path.dirname(__file__), solve_1(input), solve_2(input))
