import os
from utils.io import write_output


def read_input():
    horizontal_items_positions = []
    vertical_items_positions = []
    width = 0
    height = 0
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            line = line.strip()
            width = len(line)
            for i, item in enumerate(line):
                position = (height, i)
                if item == ">":
                    horizontal_items_positions.append(position)
                elif item == "v":
                    vertical_items_positions.append(position)
            height += 1
    return (horizontal_items_positions, vertical_items_positions, width, height)


def move_items(items_positions, matrix_dict, is_horizontal, limit):
    new_items = []
    new_matrix_dict = matrix_dict.copy()
    moved = False

    for position in items_positions:
        new_position = (
            (position[0], (position[1] + 1) % limit)
            if is_horizontal
            else ((position[0] + 1) % limit, position[1])
        )
        if new_position in matrix_dict:
            new_items.append(position)
        else:
            moved = True
            new_items.append(new_position)
            new_matrix_dict.pop(position)
            new_matrix_dict[new_position] = ">" if is_horizontal else "v"

    return (new_items, new_matrix_dict, moved)


def solve_1():
    horizontal_items_positions, vertical_items_positions, width, height = read_input()
    matrix_dict = dict()
    for x in horizontal_items_positions:
        matrix_dict[x] = ">"
    for x in vertical_items_positions:
        matrix_dict[x] = "v"

    iteration_number = 0
    while True:
        iteration_number += 1
        horizontal_items_positions, matrix_dict, has_moved_h = move_items(
            horizontal_items_positions, matrix_dict, True, width
        )
        vertical_items_positions, matrix_dict, has_moved_v = move_items(
            vertical_items_positions, matrix_dict, False, height
        )

        if not has_moved_h and not has_moved_v:
            break

    return iteration_number


def solve_2():
    # There is no part 2 for day 25
    return ""


write_output(solve_1(), solve_2())
