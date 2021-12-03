import os
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


def write_output(output_1, output_2):
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(f"{output_1}\n{output_2}")
    print(output_1, output_2)


input = read_input()
write_output(solve_1(input), solve_2(input))
