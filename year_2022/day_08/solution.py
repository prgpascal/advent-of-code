import os
from utils.io import write_output


def read_input():
    matrix = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            matrix.append([int(x) for x in line.strip()])
    return matrix


def find_visible_trees(matrix):
    result = set()
    ranges = [range(0, len(matrix)), range(len(matrix) - 1, -1, -1)]

    def is_border(i, j):
        return i in (0, len(matrix) - 1) or j in (0, len(matrix) - 1)

    for rng in ranges:
        # by row
        for i in rng:
            max = 0
            for j in rng:
                if is_border(i, j) or matrix[i][j] > max:
                    max = matrix[i][j]
                    result.add((i, j))

        # by column
        for j in rng:
            max = 0
            for i in rng:
                if is_border(i, j) or matrix[i][j] > max:
                    max = matrix[i][j]
                    result.add((i, j))

    return result


def calculate_scenic_score(matrix, row_index, col_index):
    result = 1
    by_rows = [(row_index - 1, -1, -1), (row_index + 1, len(matrix), 1)]
    by_columns = [(col_index + 1, len(matrix), 1), (col_index - 1, -1, -1)]

    # by row
    for start, stop, step in by_rows:
        count = 0
        for i in range(start, stop, step):
            count += 1
            if matrix[i][col_index] >= matrix[row_index][col_index]:
                break
        result *= count

    # by column
    for start, stop, step in by_columns:
        count = 0
        for j in range(start, stop, step):
            count += 1
            if matrix[row_index][j] >= matrix[row_index][col_index]:
                break
        result *= count

    return result


def solve_1(input):
    return len(find_visible_trees(input))


def solve_2(input):
    score = 0
    for i in range(1, len(input) - 1):
        for j in range(1, len(input) - 1):
            score = max(score, calculate_scenic_score(input, i, j))
    return score


input = read_input()
write_output(solve_1(input), solve_2(input))
