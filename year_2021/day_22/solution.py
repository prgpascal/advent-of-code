from functools import reduce
import os
import re
from collections import namedtuple
from utils.io import write_output

# Solved with the help of the Reddit community. This exercise was so challenging (>_<)"

INPUT_REGEX = r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)"
VALID_RANGE = range(-50, 51)

# The cuboid type is +1 when it's added. -1 when it's subtracted
Cuboid = namedtuple("Cuboid", ["type", "x", "y", "z"])


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            for match in re.finditer(INPUT_REGEX, line.strip()):
                input.append(
                    Cuboid(
                        1 if match.group(1) == "on" else -1,
                        (int(match.group(2)), int(match.group(3))),
                        (int(match.group(4)), int(match.group(5))),
                        (int(match.group(6)), int(match.group(7))),
                    )
                )
    return input


def is_in_range(cuboid):
    _, x, y, z = cuboid
    return (
        x[0] in VALID_RANGE
        and x[1] in VALID_RANGE
        and y[0] in VALID_RANGE
        and y[1] in VALID_RANGE
        and z[0] in VALID_RANGE
        and z[1] in VALID_RANGE
    )


def get_intersection(cuboid_1, cuboid_2):
    a = max(cuboid_1.x[0], cuboid_2.x[0])
    b = min(cuboid_1.x[1], cuboid_2.x[1])

    c = max(cuboid_1.y[0], cuboid_2.y[0])
    d = min(cuboid_1.y[1], cuboid_2.y[1])

    e = max(cuboid_1.z[0], cuboid_2.z[0])
    f = min(cuboid_1.z[1], cuboid_2.z[1])

    return (
        # The intersection will be:
        # - subtracted when the cuboid is added
        # - added when the cuboid is subtracted
        # So, the type is being inverted here
        Cuboid(cuboid_2.type * -1, (a, b), (c, d), (e, f))
        if b >= a and d >= c and f >= e
        else None
    )


def calculate_area(cuboid):
    type, x, y, z = cuboid
    # Thanks to the negative type, some cuboid areas will be subtracted
    return type * (x[1] - x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)


def solve_for_input(input):
    computed_cuboids = []
    computed_cuboids.append(input[0])

    for cuboid in input[1:]:
        to_add = []
        if cuboid.type == 1:
            to_add.append(cuboid)

        for cc in computed_cuboids:
            intersection = get_intersection(cuboid, cc)
            if intersection:
                to_add.append(intersection)

        computed_cuboids += to_add

    return reduce(lambda acc, x: acc + calculate_area(x), computed_cuboids, 0)


def solve_1():
    return solve_for_input([x for x in read_input() if is_in_range(x)])


def solve_2():
    return solve_for_input(read_input())


write_output(solve_1(), solve_2())
