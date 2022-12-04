import os
import re
from utils.io import write_output

INPUT_REGEX = r"(\d+)-(\d+),(\d+)-(\d+)"


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


def get_range_sets_from_pair(pair):
    return (
        set(list(range(pair[0][0], pair[0][1] + 1))),
        set(list(range(pair[1][0], pair[1][1] + 1))),
    )


def solve_1(input):
    count = 0
    for pair in input:
        first_range, second_range = get_range_sets_from_pair(pair)
        diff_1 = first_range.difference(second_range)
        diff_2 = second_range.difference(first_range)
        count += 1 if len(min(diff_1, diff_2)) == 0 else 0
    return count


def solve_2(input):
    count = 0
    for pair in input:
        first_range, second_range = get_range_sets_from_pair(pair)
        intersection = first_range.intersection(second_range)
        count += 1 if len(intersection) > 0 else 0
    return count


input = read_input()
write_output(solve_1(input), solve_2(input))
