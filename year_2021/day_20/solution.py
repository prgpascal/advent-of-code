import os
from collections import Counter
from utils.io import write_output


def read_input():
    matrix = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        enhancement_algorithm = list(file.readline().strip())
        file.readline()
        for line in file:
            matrix.append(list(line.strip()))
    return (enhancement_algorithm, matrix)


def expand_matrix(matrix, new_char):
    new_matrix = []
    n = len(matrix)

    for i in range(n):  # copy the matrix, and pad it with new columns
        new_matrix.append([new_char] * 2 + matrix[i] + [new_char] * 2)

    for _ in range(2):  # new rows at the beginning and end of the matrix
        new_matrix.insert(0, [new_char] * (n + 4))
        new_matrix.append([new_char] * (n + 4))

    return new_matrix


def resize_matrix(matrix):
    new_matrix = []
    for i in range(1, len(matrix) - 1):
        new_matrix.append(matrix[i][1 : len(matrix) - 1])
    return new_matrix


def get_adjacents(matrix, point):
    x, y = point
    a = matrix[x - 1][y - 1]
    b = matrix[x - 1][y]
    c = matrix[x - 1][y + 1]
    d = matrix[x][y - 1]
    e = matrix[x][y]
    f = matrix[x][y + 1]
    g = matrix[x + 1][y - 1]
    h = matrix[x + 1][y]
    i = matrix[x + 1][y + 1]
    return f"{a}{b}{c}{d}{e}{f}{g}{h}{i}"


def get_number(adj):
    binary_number = ["0" if x == "." else "1" for x in adj]
    return int("".join(str(x) for x in binary_number), 2)


def apply_enhancement_algorithm(matrix, enhancement_algorithm):
    new_matrix = matrix.copy()
    for i in range(1, len(matrix) - 1):
        new_matrix[i] = matrix[i].copy()
        for j in range(1, len(matrix) - 1):
            adj = get_adjacents(matrix, (i, j))
            number = get_number(adj)
            new_matrix[i][j] = enhancement_algorithm[number]
    return new_matrix


def solve_for_number_of_iterations(n_iterations):
    enhancement_algorithm, matrix = read_input()
    should_alternate = enhancement_algorithm[0] == "#"

    for i in range(n_iterations):
        new_char = "." if not should_alternate else "." if i % 2 == 0 else "#"
        matrix = expand_matrix(matrix, new_char)
        matrix = apply_enhancement_algorithm(matrix, enhancement_algorithm)
        matrix = resize_matrix(matrix)

    counter = Counter()
    for i in range(len(matrix)):
        counter.update(matrix[i])

    return counter["#"]


def solve_1():
    return solve_for_number_of_iterations(2)


def solve_2():
    return solve_for_number_of_iterations(50)


write_output(solve_1(), solve_2())
