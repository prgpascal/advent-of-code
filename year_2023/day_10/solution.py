import os
from utils.io import write_output
from utils.utils import sum_tuples

ADJACENT_POSITIONS = {
    "-": [(0, -1), (0, 1)],
    "|": [(-1, 0), (1, 0)],
    "7": [(0, -1), (1, 0)],
    "J": [(-1, 0), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "F": [(0, 1), (1, 0)],
}


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        matrix = [list(line.strip()) for line in file.readlines()]
        starting_position = None
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == "S":
                    starting_position = (i, j)
                    break
        return (matrix, starting_position)


def visit_perimeter(starting_position, matrix, visited: set[tuple[int, int]]):
    position = (starting_position[0], starting_position[1] + 1)
    while position not in visited:
        visited.add(position)
        symbol = matrix[position[0]][position[1]]
        if symbol == "S":
            # entire perimeter found
            return

        adj_positions = [sum_tuples(position, a) for a in ADJACENT_POSITIONS[symbol]]
        for pos in adj_positions:
            if pos not in visited:
                # found next perimeter point
                position = pos
                break


def find_internal_points(matrix):
    internal_points = set()
    external_points = set()
    for i in range(len(matrix)):
        is_internal = False
        open_tag = None
        for j in range(len(matrix[0])):
            match matrix[i][j]:
                case "|":
                    is_internal = not is_internal
                case "S":
                    pass
                case "F":
                    open_tag = "F"
                case "L":
                    open_tag = "L"
                case "7":
                    if open_tag == "L":
                        is_internal = not is_internal
                    open_tag = None
                case "J":
                    if open_tag == "F":
                        is_internal = not is_internal
                    open_tag = None
                case "-":
                    pass
                case ".":
                    if is_internal:
                        internal_points.add((i, j))
                    else:
                        external_points.add((i, j))
    return internal_points


def solve_1(input):
    matrix, starting_position = input
    visited = set([starting_position])
    visit_perimeter(starting_position, matrix, visited)
    return len(visited) // 2


def solve_2(input):
    matrix, starting_position = input
    visited = set([starting_position])
    visit_perimeter(starting_position, matrix, visited)

    # clear the points that are not part of the perimeter
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (i, j) not in visited:
                matrix[i][j] = "."

    return len(find_internal_points(matrix))


input = read_input()
write_output(solve_1(input), solve_2(input))
