import os
from collections import defaultdict
from utils.io import write_output
from math import prod
from utils.utils import get_adjacent_positions


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip() for line in file.readlines()]


def get_adjacent_symbol(i, j, matrix):
    for new_i, new_j in get_adjacent_positions(i, j, matrix):
        cell = matrix[new_i][new_j]
        if not cell.isdigit() and cell != ".":
            return (cell, (new_i, new_j))
    return (None, None)


def solve_1(input):
    part_numbers = []
    for i, line in enumerate(input):
        current_number = ""
        is_part_number = False
        for j, cell in enumerate(line):
            if cell.isdigit():
                current_number += cell
                if get_adjacent_symbol(i, j, input)[0]:
                    is_part_number = True
            else:
                if current_number != "" and is_part_number:
                    part_numbers.append(int(current_number))
                current_number = ""
                is_part_number = False

        if current_number != "" and is_part_number:
            part_numbers.append(int(current_number))

    return sum(part_numbers)


def solve_2(input):
    part_numbers = defaultdict(set)
    for i, line in enumerate(input):
        current_number = ""
        is_part_number = False
        adj_symbol_pos = (None, None)
        for j, cell in enumerate(line):
            if cell.isdigit():
                current_number += cell
                adjacent_symbol = get_adjacent_symbol(i, j, input)
                if adjacent_symbol[0] == "*":
                    is_part_number = True
                    adj_symbol_pos = adjacent_symbol[1]
            else:
                if current_number != "" and is_part_number:
                    part_numbers[adj_symbol_pos].add(int(current_number))
                current_number = ""
                is_part_number = False
                adj_symbol_pos = (None, None)

        if current_number != "" and is_part_number:
            part_numbers[adj_symbol_pos].add(int(current_number))

    products = [prod(numbers) for numbers in part_numbers.values() if len(numbers) == 2]
    return sum(products)


input = read_input()
write_output(solve_1(input), solve_2(input))
