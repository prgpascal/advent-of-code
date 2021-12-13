import os
import re
from functools import reduce
from utils.io import create_matrix, write_output

INSTRUCTION_REGEX = r"fold along ([\w+])=([\d]+)"


def read_input():
    points = set()
    fold_instructions = list()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            line = line.strip()
            if line.startswith("fold"):
                for match in re.finditer(INSTRUCTION_REGEX, line):
                    fold_instructions.append((match.group(1), int(match.group(2))))
            elif line != "":
                x, y = line.split(",")
                points.add((int(x), int(y)))
    return (points, fold_instructions)


def execute_instruction(instruction, points):
    instruction_axis = instruction[0]
    pivot = int(instruction[1])
    to_remove = set()
    to_add = set()

    if instruction_axis == "y":
        for p in points:
            if p[1] > pivot:
                new_point = (pivot * 2) - int(p[1])
                to_add.add((p[0], new_point))
                to_remove.add(p)
    else:
        for p in points:
            if p[0] > pivot:
                new_point = (pivot * 2) - int(p[0])
                to_add.add((new_point, p[1]))
                to_remove.add(p)

    points = points.union(to_add)
    points = points.difference(to_remove)
    return points


def solve_1():
    points, fold_instructions = read_input()
    points = execute_instruction(fold_instructions[0], points)
    return len(points)


def solve_2():
    points, fold_instructions = read_input()
    for instruction in fold_instructions:
        points = execute_instruction(instruction, points)

    columns = max(x for (x, _) in points) + 1
    rows = max(y for (_, y) in points) + 1
    matrix = create_matrix(rows, columns)
    for i in range(0, rows):
        for j in range(0, columns):
            if (j, i) in points:
                matrix[i][j] = "X"

    result = reduce(lambda acc, row: f"{acc}{' '.join(row)}\n", matrix, "")
    return result


write_output(solve_1(), solve_2())
