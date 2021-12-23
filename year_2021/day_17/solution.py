import os
import re
from utils.io import write_output


INPUT_REGEX = r"target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)"


def read_input():
    result = {}
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for match in re.finditer(INPUT_REGEX, file.readline().strip()):
            result = {
                "min_x": int(match.group(1)),
                "max_x": int(match.group(2)),
                "max_y": int(match.group(3)),
                "min_y": int(match.group(4)),
            }
    return result


def get_max_y(vel_x, vel_y, coordinates):
    pos_x = pos_y = 0
    max_y = 0
    is_valid = False

    while True:
        pos_x += vel_x
        pos_y += vel_y
        max_y = max(max_y, pos_y)

        if (pos_x in range(coordinates["min_x"], coordinates["max_x"] + 1)) and (
            pos_y in range(coordinates["min_y"], coordinates["max_y"] - 1, -1)
        ):
            is_valid = True
            break

        if pos_y < coordinates["max_y"]:
            # out of range
            break

        vel_x = vel_x - 1 if vel_x > 0 else vel_x + 1 if vel_x < 0 else vel_x
        vel_y -= 1

    return max_y if is_valid else None


def execute_shots():
    input = read_input()
    max_x = input["max_x"]
    max_y = input["max_y"]
    max_y_found = 0
    possible_shots = 0

    for vel_x in range(1, max_x + 1):
        for vel_y in range(max_y, abs(max_y)):
            res = get_max_y(vel_x, vel_y, input)
            if res is not None:
                max_y_found = max(max_y_found, res)
                possible_shots += 1

    return (max_y_found, possible_shots)


results = execute_shots()
write_output(results[0], results[1])
