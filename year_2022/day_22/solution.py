import os
from collections import deque
from utils.io import write_output

DIRECTIONS = ["R", "D", "L", "U"]

""" My input cube is:
     --- ---
    | 1 | 2 |
     --- ---
    | 3 |
 --- ---
| 5 | 4 |
 --- ---
| 6 |
 ---
"""

# This represents the connections between one face and the others
# key = starting face
# value = target face, reachable via a specific direction
FACES_RELATIONS = {
    1: {"U": 6, "L": 5},
    2: {"U": 6, "R": 4, "D": 3},
    3: {"R": 2, "L": 5},
    4: {"R": 2, "D": 6},
    5: {"U": 3, "L": 1},
    6: {"L": 1, "D": 2, "R": 4},
}


def read_input():
    path = ""
    matrix = []
    max_width = 0
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            if line.strip().isalnum():
                path = line.strip()
            elif line.strip() != "":
                new_row = list(line.replace("\n", "").replace(" ", "X"))
                matrix.append(new_row)
                max_width = max(max_width, len(new_row))
    for row in matrix:
        # make sure the matrix has a fixed width and height
        if len(row) < max_width:
            to_add = max_width - len(row)
            row.extend(["X"] * to_add)
    return (matrix, path)


def get_current_face(position) -> int:
    if position[0] in range(0, 50) and position[1] in range(50, 100):
        return 1
    if position[0] in range(0, 50) and position[1] in range(100, 150):
        return 2
    if position[0] in range(50, 100) and position[1] in range(50, 100):
        return 3
    if position[0] in range(100, 150) and position[1] in range(50, 100):
        return 4
    if position[0] in range(100, 150) and position[1] in range(0, 50):
        return 5
    if position[0] in range(150, 200) and position[1] in range(0, 50):
        return 6
    raise Exception("Cannot determine the current face")


def perform_move_part_1(matrix, position, direction):
    next_position = None
    match direction:
        case "R":
            next_position = (position[0], (position[1] + 1) % len(matrix[0]))
        case "L":
            next_position = (position[0], (position[1] - 1) % len(matrix[0]))
        case "U":
            next_position = ((position[0] - 1) % len(matrix), position[1])
        case "D":
            next_position = ((position[0] + 1) % len(matrix), position[1])
    if next_position is None:
        raise Exception("Cannot compute the next position")

    if matrix[next_position[0]][next_position[1]] == "#":
        return None
    elif matrix[next_position[0]][next_position[1]] == "X":
        return perform_move_part_1(matrix, next_position, direction)
    else:
        return next_position


def perform_move_part_2(matrix, position, direction, current_face=None):
    next_position = None
    next_direction = direction
    if current_face is None:
        current_face = get_current_face(position)

    match direction:
        case "R":
            next_position = (position[0], (position[1] + 1))
        case "L":
            next_position = (position[0], (position[1] - 1))
        case "U":
            next_position = ((position[0] - 1), position[1])
        case "D":
            next_position = ((position[0] + 1), position[1])
    if next_position is None:
        raise Exception("Cannot compute the next position")

    if (
        (next_position[0] not in range(0, len(matrix)))
        or (next_position[1] not in range(0, len(matrix[0])))
        or (matrix[next_position[0]][next_position[1]] == "X")
    ):
        new_face = FACES_RELATIONS[current_face][direction]
        match (current_face, new_face):
            case (1, 6):
                next_position = (150 + (next_position[1] - 50), -1)
                next_direction = "R"
            case (1, 5):
                next_position = (149 - next_position[0], -1)
                next_direction = "R"
            case (2, 6):
                next_position = (200, next_position[1] - 100)
                next_direction = "U"
            case (2, 4):
                next_position = (100 + (49 - next_position[0]), 100)
                next_direction = "L"
            case (2, 3):
                next_position = (50 + (next_position[1] - 100), 100)
                next_direction = "L"
            case (3, 2):
                next_position = (50, 100 + (next_position[0] - 50))
                next_direction = "U"
            case (3, 5):
                next_position = (99, next_position[0] - 50)
                next_direction = "D"
            case (4, 2):
                next_position = (149 - next_position[0], 150)
                next_direction = "L"
            case (4, 6):
                next_position = (150 + (next_position[1] - 50), 50)
                next_direction = "L"
            case (5, 3):
                next_position = (50 + next_position[1], 49)
                next_direction = "R"
            case (5, 1):
                next_position = (149 - next_position[0], 49)
                next_direction = "R"
            case (6, 1):
                next_position = (-1, 50 + (next_position[0] - 150))
                next_direction = "D"
            case (6, 2):
                next_position = (-1, 100 + next_position[1])
                next_direction = "D"
            case (6, 4):
                next_position = (150, 50 + (next_position[0] - 150))
                next_direction = "U"
        return perform_move_part_2(matrix, next_position, next_direction, current_face)
    elif matrix[next_position[0]][next_position[1]] == "#":
        return (None, None)
    else:
        return (next_position, next_direction)


def move(matrix, position, direction, path: deque, is_part_2=False):
    while len(path) > 0:
        if path[0].isdigit():
            tmp_steps = ""
            while len(path) > 0 and path[0].isdigit():
                tmp_steps += path.popleft()
            steps_count = int(tmp_steps)

            for _ in range(steps_count):
                new_direction = direction
                if not is_part_2:
                    new_position = perform_move_part_1(matrix, position, direction)
                else:
                    new_position, new_direction = perform_move_part_2(
                        matrix, position, direction
                    )

                if new_position is None or new_direction is None:
                    # cannot move to the new position
                    break

                # move succeeded, update the position and the direction
                if new_position is not None:
                    position = new_position
                if new_direction is not None:
                    direction = new_direction
        else:
            match path.popleft():
                case "R":
                    direction = DIRECTIONS[
                        (DIRECTIONS.index(direction) + 1) % len(DIRECTIONS)
                    ]
                case "L":
                    direction = DIRECTIONS[
                        (DIRECTIONS.index(direction) - 1) % len(DIRECTIONS)
                    ]
    return (position, direction)


def solve(is_part_2):
    matrix, path = read_input()
    start_position = (0, matrix[0].index("."))
    position, direction = move(matrix, start_position, "R", deque(path), is_part_2)
    return (
        (1000 * (position[0] + 1))
        + (4 * (position[1] + 1))
        + DIRECTIONS.index(direction)
    )


def solve_1():
    return solve(False)


def solve_2():
    return solve(True)


write_output(solve_1(), solve_2())
