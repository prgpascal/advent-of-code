import os
from utils.io import write_output


def read_input():
    groups = []
    current_group = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            line = line.strip()
            if line == "":
                groups.append(current_group)
                current_group = []
            else:
                current_group.append(int(line))
    groups.append(current_group)
    return groups


def solve_1(input):
    sums = [sum(group) for group in input]
    return max(sums)


def solve_2(input):
    sums = sorted([sum(group) for group in input])
    return sum(sums[-3:])


input = read_input()
write_output(solve_1(input), solve_2(input))
