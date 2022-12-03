import os
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip() for line in file.readlines()]


def calculate_priority(item: str):
    return ord(item) - 96 if item.islower() else ord(item) - 38


def solve_1(input):
    sum = 0
    for rucksack in input:
        middle_index = len(rucksack) // 2
        first_compartment = set(rucksack[:middle_index])
        second_compartment = set(rucksack[middle_index:])
        common_item = first_compartment.intersection(second_compartment)
        sum += calculate_priority(common_item.pop())
    return sum


def solve_2(input):
    group = []
    sum = 0
    for i, rucksack in enumerate(input):
        group.append(set(rucksack))
        if i != 0 and (i + 1) % 3 == 0:
            # the group is full, find the common item
            common_item = group[0].intersection(group[1]).intersection(group[2])
            sum += calculate_priority(common_item.pop())
            group = []
    return sum


input = read_input()
write_output(solve_1(input), solve_2(input))
