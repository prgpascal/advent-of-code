import os
from collections import deque
from utils.io import create_matrix, write_output
from utils.data_structures import Point

SHAPES = {
    0: [list("@@@@")],
    1: [
        list(".@."),
        list("@@@"),
        list(".@."),
    ],
    2: [
        list("..@"),
        list("..@"),
        list("@@@"),
    ],
    3: [
        list("@"),
        list("@"),
        list("@"),
        list("@"),
    ],
    4: [
        list("@@"),
        list("@@"),
    ],
}


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return file.readline().strip()


def can_move_to(matrix, shape, shape_position):
    if (
        len(shape[0]) + shape_position.x > len(matrix[0])
        or (shape_position.y >= len(matrix))
        or (shape_position.x < 0)
    ):
        return False

    for row, _ in enumerate(shape):
        for col, _ in enumerate(shape[0]):
            x_in_matrix = col + shape_position.x
            y_in_matrix = row + shape_position.y
            if y_in_matrix not in range(len(matrix)):
                return False
            if shape[row][col] == "@" and matrix[y_in_matrix][x_in_matrix] == "#":
                return False
    return True


def apply_projection(matrix, shape, shape_position):
    for row, _ in enumerate(shape):
        for col, _ in enumerate(shape[0]):
            if shape[row][col] == "@":
                matrix[row + shape_position.y][col + shape_position.x] = "#"


def get_empty_lines_from_top(matrix):
    tallest = 0
    while tallest < len(matrix) and "#" not in matrix[tallest]:
        tallest += 1
    return tallest


def get_height(input, rocks_number, is_part_2):
    matrix = deque()
    movements_done = 0
    finished_rocks = 0
    new_shape = SHAPES[0]

    part_2_height = 0
    part_2_rocks = 0
    part_2_current_height = 0

    while True:
        if finished_rocks == rocks_number:
            break

        # FOR PART #2
        if is_part_2:
            if movements_done % len(input) == 0:
                tallest = get_empty_lines_from_top(matrix)
                height = len(matrix) - tallest
                if part_2_height == 0:
                    part_2_height += height
                    part_2_rocks += finished_rocks
                else:
                    diff_height = height - part_2_height
                    diff_rocks = finished_rocks - part_2_rocks
                    remaining = rocks_number - part_2_rocks
                    count = remaining // diff_rocks
                    remaining_after = remaining - (count * diff_rocks)
                    new_height = count * diff_height
                    part_2_height += new_height
                    part_2_rocks += count * diff_rocks
                    finished_rocks = rocks_number - remaining_after
                    part_2_current_height = len(matrix) - get_empty_lines_from_top(
                        matrix
                    )

        # remove additional empty spaces
        tallest = get_empty_lines_from_top(matrix)
        if tallest > 3:
            for _ in range(tallest - 3):
                matrix.popleft()

        # add additional empty spaces
        matrix.extendleft(create_matrix((3 - tallest), 7, "."))

        # add spaces occupied by current shape
        matrix.extendleft(create_matrix(len(new_shape), 7, "."))
        shape_x = 2
        shape_y = 0

        while True:
            # Move horizontally
            move = input[movements_done % len(input)]
            if move == ">":
                if can_move_to(matrix, new_shape, Point(shape_x + 1, shape_y)):
                    shape_x += 1
            else:
                if can_move_to(matrix, new_shape, Point(shape_x - 1, shape_y)):
                    shape_x -= 1

            movements_done += 1

            # Move vertically
            if can_move_to(matrix, new_shape, Point(shape_x, shape_y + 1)):
                shape_y += 1
            else:
                apply_projection(matrix, new_shape, Point(shape_x, shape_y))
                finished_rocks += 1
                new_shape = SHAPES[finished_rocks % len(SHAPES)]
                break

    if not is_part_2:
        return len(matrix) - get_empty_lines_from_top(matrix)

    return part_2_height + (
        len(matrix) - get_empty_lines_from_top(matrix) - part_2_current_height
    )


def solve_1(input):
    return get_height(input, 2022, False)


def solve_2(input):
    return get_height(input, 1000000000000, True)


input = read_input()
write_output(solve_1(input), solve_2(input))
