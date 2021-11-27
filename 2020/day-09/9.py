import os
from collections import deque

PREAMBLE = 25


def read_input():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [int(l.strip()) for l in f.readlines()]
    return lines


def check_sum_of_numbers(numbers, expected_sum):
    for x, y in ((x, y) for x in numbers for y in numbers):
        if x + y == expected_sum:
            return True
    return False


def solve_1(lines):
    numbers = deque(lines[:PREAMBLE], maxlen=PREAMBLE)
    for num in lines[PREAMBLE:]:
        if not check_sum_of_numbers(numbers, num):
            return num
        numbers.append(num)


def solve_2(lines, invalid_number):
    numbers = deque()
    for num in lines:
        numbers.append(num)
        numbers_sum = sum(numbers)
        while numbers_sum > invalid_number:
            numbers_sum -= numbers.popleft()

        if numbers_sum == invalid_number:
            return numbers


lines = read_input()
invalid_number = solve_1(lines)
print(invalid_number)
solution_range = solve_2(lines, invalid_number)
print(min(solution_range) + max(solution_range))
