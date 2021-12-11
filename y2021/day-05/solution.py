import os
from collections import Counter
import re

INPUT_REGEX = r"(\d+),(\d+) -> (\d+),(\d+)"


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            for match in re.finditer(INPUT_REGEX, line.strip()):
                input.append(
                    [
                        (int(match.group(1)), int(match.group(2))),
                        (int(match.group(3)), int(match.group(4))),
                    ]
                )

    return input


def get_start_end_point_from_line(line):
    start_point, end_point = line
    start, end = line

    if is_horizontal_or_vertical_line(start_point, end_point):
        if start_point[0] > end_point[0] or start_point[1] > end_point[1]:
            start = end_point
            end = start_point
    elif is_diagonal_line(start_point, end_point):
        if start_point[0] > end_point[0]:
            start = end_point
            end = start_point

    return (start, end)


def is_horizontal_or_vertical_line(start_point, end_point):
    return start_point[0] == end_point[0] or start_point[1] == end_point[1]


def is_diagonal_line(start_point, end_point):
    return abs(start_point[0] - end_point[0]) == abs(start_point[1] - end_point[1])


def is_diagonal_increasing(start_point, end_point):
    return start_point[1] < end_point[1]


def solve_1(input):
    count = Counter()

    for line in input:
        start_point, end_point = get_start_end_point_from_line(line)

        if is_horizontal_or_vertical_line(start_point, end_point):
            for x in range(start_point[0], end_point[0] + 1):
                for y in range(start_point[1], end_point[1] + 1):
                    count.update([(x, y)])

    return len([x for x in count.items() if x[1] >= 2])


def solve_2(input):
    count = Counter()

    for line in input:
        start_point, end_point = get_start_end_point_from_line(line)

        if is_horizontal_or_vertical_line(start_point, end_point):
            for x in range(start_point[0], end_point[0] + 1):
                for y in range(start_point[1], end_point[1] + 1):
                    count.update([(x, y)])

        elif is_diagonal_line(start_point, end_point):
            touched_point = start_point
            count.update([touched_point])
            while touched_point != end_point:
                touched_point = (
                    (touched_point[0] + 1, touched_point[1] + 1)
                    if is_diagonal_increasing(start_point, end_point)
                    else (touched_point[0] + 1, touched_point[1] - 1)
                )
                count.update([touched_point])

    return len([x for x in count.items() if x[1] >= 2])


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
write_output(solve_1(input), solve_2(input))
