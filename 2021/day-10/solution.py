import os
from functools import reduce
import bisect

OPENING_CHARS_DICT = {"(": ")", "[": "]", "{": "}", "<": ">"}
CLOSING_CHARS_DICT = {")": "(", "]": "[", "}": "{", ">": "<"}


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = [line.strip() for line in file.readlines()]
    return input


def solve_1(input):
    POINTS_DICT = {")": 3, "]": 57, "}": 1197, ">": 25137}
    corrupted_chars = []
    corrupted_lines = []

    for line in input:
        stack = []
        for char in list(line):
            if char in CLOSING_CHARS_DICT:
                last_char_found = stack.pop()
                if last_char_found != CLOSING_CHARS_DICT[char]:
                    corrupted_chars.append(char)
                    corrupted_lines.append(line)
                    break
            else:
                stack.append(char)

    return (
        reduce(lambda acc, x: acc + POINTS_DICT[x], corrupted_chars, 0),
        corrupted_lines,
    )


def solve_2(input, corrupted_lines):
    POINTS_DICT = {")": 1, "]": 2, "}": 3, ">": 4}
    all_opening_chars = []

    for line in input:
        if line not in corrupted_lines:
            stack = []
            for char in list(line):
                if char in CLOSING_CHARS_DICT:
                    stack.pop()
                else:
                    stack.append(char)
            all_opening_chars.append(stack.copy())

    scores = []
    for opening_chars in all_opening_chars:
        closing_chars = [OPENING_CHARS_DICT[c] for c in reversed(opening_chars)]
        bisect.insort(
            scores, reduce(lambda acc, x: (acc * 5) + POINTS_DICT[x], closing_chars, 0)
        )

    return scores[int(len(scores) / 2)]


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
output_1, corrupted_lines = solve_1(input)
output_2 = solve_2(input, corrupted_lines)
write_output(output_1, output_2)
