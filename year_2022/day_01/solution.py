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
        if len(current_group) > 0:
            groups.append(current_group)
    return groups


def solve_1():
    groups = read_input()
    sums = [sum(group) for group in groups]
    return max(sums)


def solve_2():
    groups = read_input()
    sums = sorted([sum(group) for group in groups])
    return sum(sums[-3:])


write_output(solve_1(), solve_2())
