import os
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [int(x) for x in file.readline().strip().split(",")]


def solve_for_day(input, day):
    fishes_list = input.copy()
    fishes_per_timer = [0] * 9
    for fish in fishes_list:
        fishes_per_timer[fish] += 1

    for _ in range(day):
        number_of_new_fishes = fishes_per_timer[0]
        for index in range(1, 9):
            fishes_per_timer[index - 1] = fishes_per_timer[index]
        fishes_per_timer[6] += number_of_new_fishes
        fishes_per_timer[8] = number_of_new_fishes

    return sum(fishes_per_timer)


def solve_1():
    return solve_for_day(read_input(), 80)


def solve_2():
    return solve_for_day(read_input(), 256)


write_output(solve_1(), solve_2())
