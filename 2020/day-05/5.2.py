import math
import os
from collections import deque
from typing import Deque, Sequence


def get_input() -> Sequence:
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]
    return lines


def get_row(start: int, end: int, steps: Deque):
    if start == end:
        return start

    step = steps.popleft()
    middle = (start + end) / 2

    if step == "F" or step == "L":
        return get_row(start, math.floor(middle), steps)
    else:
        return get_row(math.ceil(middle), end, steps)


def solve():
    seat_ids = set()
    for line in get_input():
        row = get_row(0, 127, deque(line[:7]))
        column = get_row(0, 7, deque(line[7:]))
        seat_ids.add((row*8)+column)

    for i in range(min(seat_ids), max(seat_ids)):
        if i not in seat_ids:
            return i


print(solve())
