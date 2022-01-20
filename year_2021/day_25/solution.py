import os
from utils.analysis import clock
from utils.io import create_matrix, print_matrix, write_output


def read_input():
    line_number = 0
    horizontal_items_positions = []
    vertical_items_positions = []
    width = 0
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            line = line.strip()
            width = len(line)
            for i, item in enumerate(line):
                position = (line_number, i)
                if item == ">":
                    horizontal_items_positions.append(position)
                elif item == "v":
                    vertical_items_positions.append(position)
            line_number += 1
    return (horizontal_items_positions, vertical_items_positions, width, line_number)


def pretty_print(matrix_dict, width, height):
    matrix = create_matrix(height, width, char=".")
    for x, y in matrix_dict.items():
        matrix[x[0]][x[1]] = y
    print_matrix(matrix, as_string=True)


def move_items(items_positions, matrix_dict, is_horizontal, limit):
    new_items = []
    new_dict = matrix_dict.copy()  # TODO: avoid copy
    has_moved = False

    for position in items_positions:
        new_position = (
            (position[0], (position[1] + 1) % limit)
            if is_horizontal
            else ((position[0] + 1) % limit, position[1])
        )
        if new_position in matrix_dict:
            new_items.append(position)
        else:
            has_moved = True
            new_items.append(new_position)
            new_dict.pop(position)
            new_dict[new_position] = ">" if is_horizontal else "v"

    return (new_items, new_dict, has_moved)


@clock()
def solve_1():
    horizontal_items_positions, vertical_items_positions, width, height = read_input()
    matrix_dict = dict()
    for x in horizontal_items_positions:
        matrix_dict[x] = ">"
    for x in vertical_items_positions:
        matrix_dict[x] = "v"

    iteration_number = 0
    while True:
        horizontal_items_positions, matrix_dict, has_moved_h = move_items(
            horizontal_items_positions, matrix_dict, True, width
        )
        vertical_items_positions, matrix_dict, has_moved_v = move_items(
            vertical_items_positions, matrix_dict, False, height
        )

        if not has_moved_h and not has_moved_v:
            break

        iteration_number += 1

    return iteration_number + 1


def solve_2():
    input = read_input()
    return ""


write_output(solve_1(), solve_2())
