import os
from utils.io import write_output
from math import prod


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        races = [int(x) for x in line1.split(":")[1].split(" ") if x != ""]
        distances = [int(x) for x in line2.split(":")[1].split(" ") if x != ""]
        return list(zip(races, distances))


def can_beat_record(hold_time, record_distance, max_time):
    speed = hold_time
    time_remaining = max_time - hold_time
    new_distance = speed * time_remaining
    return new_distance > record_distance


def find_winning_range(record_distance, max_time):
    """The winning races have gaussian distribution, so find the min and max hold_times that
    allows us to win."""
    left_index = 0
    right_index = 0
    for hold_time in range(max_time + 1):
        if can_beat_record(hold_time, record_distance, max_time):
            left_index = hold_time
            break
    for hold_time in reversed(range(max_time + 1)):
        if can_beat_record(hold_time, record_distance, max_time):
            right_index = hold_time
            break
    return (left_index, right_index)


def solve_1(input):
    winning_ways = []
    for max_time, record_distance in input:
        left_index, right_index = find_winning_range(record_distance, max_time)
        winning_ways.append(right_index - left_index + 1)
    return prod(winning_ways)


def solve_2(input):
    max_time = int("".join(str(t[0]) for t in input))
    record_distance = int("".join(str(t[1]) for t in input))
    left_index, right_index = find_winning_range(record_distance, max_time)
    return right_index - left_index + 1


input = read_input()
write_output(solve_1(input), solve_2(input))
