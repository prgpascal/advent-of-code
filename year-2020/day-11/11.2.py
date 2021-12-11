import os


def read_input():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    matrix = []
    with open(file_path) as f:
        for line in (line.strip() for line in f):
            matrix.append(list(line))
    return matrix


def get_first_visible_seats_from_position(matrix, i, j):
    iteration_number = 1
    result = []
    finished_directions = set()
    while len(finished_directions) < 8:
        adjacent_positions = [
            (i-iteration_number, j-iteration_number),
            (i-iteration_number, j),
            (i-iteration_number, j+iteration_number),
            (i, j-iteration_number),
            (i, j+iteration_number),
            (i+iteration_number, j-iteration_number),
            (i+iteration_number, j),
            (i+iteration_number, j+iteration_number)
        ]

        for pos, (x, y) in enumerate(adjacent_positions):
            if pos not in finished_directions:
                if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]):
                    if matrix[x][y] != ".":
                        result.append(matrix[x][y])
                        finished_directions.add(pos)
                else:
                    finished_directions.add(pos)

        iteration_number += 1

    return result


def apply_rules(matrix):
    new_matrix = [[0 for _ in range(len(matrix[0]))]
                  for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != ".":
                adjacent_seats = get_first_visible_seats_from_position(
                    matrix, i, j)
                occupied_seats_count = adjacent_seats.count("#")
                if matrix[i][j] == "L" and occupied_seats_count == 0:
                    new_matrix[i][j] = "#"
                elif matrix[i][j] == "#" and occupied_seats_count >= 5:
                    new_matrix[i][j] = "L"
                else:
                    new_matrix[i][j] = matrix[i][j]
            else:
                new_matrix[i][j] = matrix[i][j]
    return new_matrix


def count_occupied_seats(matrix):
    return sum(line.count("#") for line in matrix)


def solve(matrix):
    previous_occupied_seats = 0
    while True:
        matrix = apply_rules(matrix)
        occupied_seats = count_occupied_seats(matrix)
        if occupied_seats == previous_occupied_seats:
            break
        previous_occupied_seats = occupied_seats
    return occupied_seats


print(solve(read_input()))
