import os


def read_input():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    matrix = []
    with open(file_path) as f:
        for line in (line.strip() for line in f):
            matrix.append(list(line))
    return matrix


def get_adjacent_seats(matrix, i, j):
    adjacent_positions = [
        (i-1, j-1),
        (i-1, j),
        (i-1, j+1),
        (i, j-1),
        (i, j+1),
        (i+1, j-1),
        (i+1, j),
        (i+1, j+1)
    ]
    result = []
    for x, y in adjacent_positions:
        if x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0]):
            result.append(matrix[x][y])
    return result


def count_seats_types(seats, type):
    return len([s for s in seats if s == type])


def apply_rules(matrix):
    new_matrix = [[0 for _ in range(len(matrix[0]))]
                  for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            adjacent_seats = get_adjacent_seats(matrix, i, j)
            if matrix[i][j] == "L" and count_seats_types(adjacent_seats, "#") == 0:
                new_matrix[i][j] = "#"
            elif matrix[i][j] == "#" and count_seats_types(adjacent_seats, "#") >= 4:
                new_matrix[i][j] = "L"
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


matrix = read_input()
print(solve(matrix))
