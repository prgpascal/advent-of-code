import os
from collections import deque

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"
FRONT = "F"
RIGHT = "R"
LEFT = "L"


def read_input():
    file_path = os.path.join(os.path.dirname(__file__), "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [(l.strip()[0], int(l.strip()[1:])) for l in f.readlines()]
    return lines


def solve_1(operations):
    direction = EAST
    x = y = 0
    compass = deque(
        (
            EAST,
            SOUTH,
            WEST,
            NORTH,
        )
    )

    for dir, num in operations:
        if dir == FRONT:
            dir = direction

        if dir == NORTH:
            y -= num
        elif dir == SOUTH:
            y += num
        elif dir == EAST:
            x += num
        elif dir == WEST:
            x -= num
        elif dir == RIGHT:
            compass.rotate(int(-num / 90))
        elif dir == LEFT:
            compass.rotate(int(num / 90))

        direction = compass[0]

    return (x, y)


def solve_2(operations):
    ship_pos = [0, 0]
    waypoint_pos = [10, -1]

    for dir, num in operations:
        if dir == FRONT:
            ship_pos[0] += waypoint_pos[0] * num
            ship_pos[1] += waypoint_pos[1] * num
        elif dir == NORTH:
            waypoint_pos[1] -= num
        elif dir == SOUTH:
            waypoint_pos[1] += num
        elif dir == EAST:
            waypoint_pos[0] += num
        elif dir == WEST:
            waypoint_pos[0] -= num
        else:
            compass = deque([waypoint_pos[0], waypoint_pos[1], 0, 0])
            if dir == RIGHT:
                compass.rotate(int(num / 90))
            elif dir == LEFT:
                compass.rotate(int(-num / 90))
            waypoint_pos[0] = compass[0] if compass[0] != 0 else compass[2] * -1
            waypoint_pos[1] = compass[1] if compass[1] != 0 else compass[3] * -1

    return ship_pos


operations = read_input()
solution = solve_1(operations)
print(abs(solution[0]) + abs(solution[1]))

solution = solve_2(operations)
print(abs(solution[0]) + abs(solution[1]))
