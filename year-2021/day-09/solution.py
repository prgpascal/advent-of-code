import math
import os
from functools import reduce


def read_input():
    matrix = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            matrix.append([int(x) for x in list(line.strip())])

    return matrix


def find_low_points(matrix):
    low_points = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            adjacent_points = []
            if i > 0:
                adjacent_points.append(matrix[i - 1][j])
            if i < len(matrix) - 1:
                adjacent_points.append(matrix[i + 1][j])
            if j > 0:
                adjacent_points.append(matrix[i][j - 1])
            if j < len(matrix[i]) - 1:
                adjacent_points.append(matrix[i][j + 1])

            if matrix[i][j] < min(adjacent_points):
                low_points.append((matrix[i][j], i, j))

    return low_points


def find_basin(x, y, matrix, found):
    if (
        (x not in range(len(matrix)) or y not in range(len(matrix[0])))
        or matrix[x][y] == 9
        or (x, y) in found
    ):
        # (x, y) is not a valid point or has already been found
        return

    found.add((x, y))

    find_basin(x - 1, y, matrix, found)
    find_basin(x + 1, y, matrix, found)
    find_basin(x, y - 1, matrix, found)
    find_basin(x, y + 1, matrix, found)


def solve_1(matrix):
    low_points = find_low_points(matrix)
    low_points_sum = reduce(lambda accumulator, x: accumulator + x[0], low_points, 0)

    return low_points_sum + len(low_points)


def solve_2(matrix):
    low_points = find_low_points(matrix)
    basins = []
    for point in low_points:
        found = set()
        find_basin(point[1], point[2], matrix, found)
        basins.append(len(found))

    return math.prod(sorted(basins)[-3:])


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
write_output(solve_1(input), solve_2(input))
