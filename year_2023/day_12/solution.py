import os
import re
from functools import cache
from utils.io import write_output

# Part #2 solved with the help of the Reddit community. This exercise was so challenging (>_<)"
# Credits: https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kd221yp


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            sequence, occurrences = line.strip().split(" ")
            occurrences = [int(x) for x in occurrences.split(",")]
            input.append((sequence, occurrences))
        return input


def build_regex(occurrences):
    return "^[.?]*" + "[.?]+".join(f"[?#]{{{occ}}}" for occ in occurrences) + "[.?]*$"


@cache
def find_arrangements(sequence: str, occurrences: tuple):
    if not occurrences:
        return 1 if "#" not in sequence else 0

    result = 0
    current, occurrences = occurrences[0], occurrences[1:]
    for i in range(len(sequence) - sum(occurrences) - len(occurrences) - current + 1):
        if "#" in sequence[:i]:
            break
        if (
            (next := i + current) <= len(sequence)
            and "." not in sequence[i:next]
            and sequence[next : next + 1] != "#"
        ):
            result += find_arrangements(sequence[next + 1 :], occurrences)

    return result


def solve_1(input):
    found = []
    for sequence, occurrences in input:
        regex = build_regex(occurrences)
        queue = [sequence]
        while len(queue) > 0:
            item = queue.pop()
            if "?" not in item:
                found.append(item)
                continue

            # evaluate both alternatives: "#" and "."
            v1 = item.replace("?", "#", 1)
            v2 = item.replace("?", ".", 1)

            if re.match(regex, v1):
                queue.append(v1)
            if re.match(regex, v2):
                queue.append(v2)

    return len(found)


def solve_2(input):
    result = 0
    for sequence, occurrences in input:
        extended_sequence = "?".join([sequence] * 5)
        extended_occurrences = occurrences * 5
        result += find_arrangements(extended_sequence, tuple(extended_occurrences))
    return result


input = read_input()
write_output(solve_1(input), solve_2(input))
