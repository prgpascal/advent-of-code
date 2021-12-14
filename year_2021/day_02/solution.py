import os
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            command, value = line.strip().split(" ")
            input.append((command, int(value)))
    return input


def solve_1():
    input = read_input()
    x_axis_value = 0
    y_axis_value = 0
    for (command, value) in input:
        if command == "forward":
            x_axis_value += value
        elif command == "down":
            y_axis_value += value
        else:
            y_axis_value -= value
    return x_axis_value * y_axis_value


def solve_2():
    input = read_input()
    x_axis_value = 0
    y_axis_value = 0
    aim = 0
    for (command, value) in input:
        if command == "forward":
            x_axis_value += value
            y_axis_value += aim * value
        elif command == "down":
            aim += value
        else:
            aim -= value
    return x_axis_value * y_axis_value


write_output(solve_1(), solve_2())
