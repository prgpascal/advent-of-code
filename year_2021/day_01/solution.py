import os
from collections import deque
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = [int(line.strip()) for line in file.readlines()]
    return input


def solve_1():
    input = read_input()
    previous = input[0]
    counter = 0
    for current in input:
        if current > previous:
            counter += 1
        previous = current
    return counter


def solve_2():
    input = read_input()
    window = deque(maxlen=3)
    previous_sum = sum(input[0:3])
    counter = 0
    for current in input:
        window.append(current)
        if len(window) == 3:
            current_sum = sum(window)
            if current_sum > previous_sum:
                counter += 1
            previous_sum = current_sum
    return counter


write_output(solve_1(), solve_2())
