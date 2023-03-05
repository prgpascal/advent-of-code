import os
from collections import deque
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return file.readline().strip()


def solve(input, distinct_chars):
    buffer = deque(maxlen=distinct_chars)
    for i, char in enumerate(input, start=1):
        buffer.append(char)
        if len(set(buffer)) == distinct_chars:
            return i


def solve_1(input):
    return solve(input, 4)


def solve_2(input):
    return solve(input, 14)


input = read_input()
write_output(solve_1(input), solve_2(input))
