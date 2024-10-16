import os
from utils.io import get_matrix_column, write_output
from utils.utils import hamming_distance


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        matrices = []
        matrix = []
        for line in file:
            line = line.strip()
            if line != "":
                matrix.append(line)
            else:
                matrices.append(matrix)
                matrix = []

        matrices.append(matrix)
        return matrices


def calculate_result(found):
    return sum(
        [
            *[(x[1] + 1) for x in found if x[0] == "vertical"],
            *[(x[1] + 1) * 100 for x in found if x[0] == "horizontal"],
        ]
    )


def solve_1(input):
    result = []
    for matrix in input:
        n_rows = len(matrix)
        n_cols = len(matrix[0])

        # horizontal search
        for reflection_line in range(n_rows - 1):
            if matrix[reflection_line] == matrix[reflection_line + 1]:
                i = 0
                while True:
                    i += 1
                    x = reflection_line - i
                    y = reflection_line + i + 1
                    if x < 0 or y >= n_rows:
                        # limit reached
                        result.append(("horizontal", reflection_line))
                        break

                    if matrix[x] != matrix[y]:
                        # found two different rows
                        break

        # vertical search
        for reflection_line in range(n_cols - 1):
            if get_matrix_column(matrix, reflection_line) == get_matrix_column(
                matrix, reflection_line + 1
            ):
                i = 0
                while True:
                    i += 1
                    x = reflection_line - i
                    y = reflection_line + i + 1
                    if x < 0 or y >= n_cols:
                        # limit reached
                        result.append(("vertical", reflection_line))
                        break

                    if get_matrix_column(matrix, x) != get_matrix_column(matrix, y):
                        # found two different columns
                        break

    return calculate_result(result)


def solve_2(input):
    result = []
    for matrix in input:
        n_rows = len(matrix)
        n_cols = len(matrix[0])

        # horizontal search
        for line in range(n_rows - 1):
            hamming = hamming_distance(matrix[line], matrix[line + 1])
            if hamming in [0, 1]:
                i = 0
                has_fixed_smudge = hamming != 0

                while True:
                    i += 1
                    x = line - i
                    y = line + i + 1
                    if x < 0 or y >= n_rows:
                        # limit reached
                        if has_fixed_smudge:
                            result.append(("horizontal", line))
                        break

                    if matrix[x] != matrix[y] and has_fixed_smudge:
                        # smudge was already fixed
                        break

                    if matrix[x] != matrix[y] and not has_fixed_smudge:
                        # found two different rows
                        distance = hamming_distance(matrix[x], matrix[y])
                        if distance == 1:
                            has_fixed_smudge = True
                        else:
                            break

        # vertical search
        for line in range(n_cols - 1):
            col_1 = get_matrix_column(matrix, line)
            col_2 = get_matrix_column(matrix, line + 1)
            if col_1 == col_2 or hamming_distance(col_1, col_2) == 1:
                # this can be an incidence point
                i = 0
                has_fixed_smudge = hamming_distance(col_1, col_2) != 0

                while True:
                    i += 1
                    x = line - i
                    y = line + i + 1
                    if x < 0 or y >= n_cols:
                        # limit reached
                        if has_fixed_smudge:
                            result.append(("vertical", line))
                        break

                    if (
                        get_matrix_column(matrix, x) != get_matrix_column(matrix, y)
                        and has_fixed_smudge
                    ):
                        break

                    if (
                        get_matrix_column(matrix, x) != get_matrix_column(matrix, y)
                        and not has_fixed_smudge
                    ):
                        # found two different columns
                        distance = hamming_distance(
                            get_matrix_column(matrix, x), get_matrix_column(matrix, y)
                        )
                        if distance == 1:
                            has_fixed_smudge = True
                        else:
                            break

    return calculate_result(result)


input = read_input()
write_output(solve_1(input), solve_2(input))
