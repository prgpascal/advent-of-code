import os
from utils.io import write_output
import numpy as np


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [list(line.strip()) for line in file.readlines()]


def move_north(input):
    for i in range(len(input)):
        for j in range(len(input[0])):
            if input[i][j] == "O":
                start_index = i
                top_index = start_index - 1
                while top_index >= 0 and input[top_index][j] == ".":
                    # move north
                    input[top_index][j] = "O"
                    input[start_index][j] = "."
                    start_index -= 1
                    top_index -= 1
    return input


def rotate_matrix(matrix):
    return np.rot90(matrix, k=1, axes=(1, 0))


def calculate_result(matrix):
    result = 0
    for i, row in enumerate(matrix):
        result += list(row).count("O") * (len(matrix) - i)
    return result


def solve_1(matrix):
    return calculate_result(move_north(matrix))


def solve_2(matrix):
    """By analyzing the intermediate results, I found that after some cycles, the
    total load on the north support beams repeats.
    I found the starting value of that cycle, and fine-tuned the number of cycles
    required to discover the index of the first value of first cycle.
    """
    n_discovery_cycles = 150
    cycle_length = 13
    first_cycle_value = 87286

    # find the index of the first cycle value
    results = []
    cycle_start_index = -1
    for i in range(n_discovery_cycles):
        matrix = move_north(matrix)  # top
        matrix = move_north(rotate_matrix(matrix))  # left
        matrix = move_north(rotate_matrix(matrix))  # bottom
        matrix = move_north(rotate_matrix(matrix))  # right
        matrix = rotate_matrix(matrix)  # top (again)

        result = calculate_result(matrix)
        results.append((i + 1, result))
        # print(i + 1, res) # used for analysis
        if result == first_cycle_value and cycle_start_index == -1:
            cycle_start_index = i

    cycle_end_index = cycle_start_index + cycle_length
    normalized_results = {
        x[0]: x[1] for x in results[cycle_start_index:cycle_end_index]
    }

    for k in normalized_results.keys():
        if k % cycle_length == 1000000000 % cycle_length:
            return normalized_results[k]


write_output(solve_1(read_input()), solve_2(read_input()))
