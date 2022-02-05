import os
from collections import Counter
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [int(x) for x in file.readline().strip().split(",")]


def solve_1():
    input = read_input()
    crabs_counter = Counter(input)
    crabs_positions = list(set(input))
    computed_fuels = Counter()

    for position in crabs_positions:
        fuels = [
            n_crabs * abs(crab_pos - position)
            for crab_pos, n_crabs in crabs_counter.items()
        ]
        computed_fuels[position] = sum(fuels)

    return computed_fuels.most_common()[-1][1]


def solve_2():
    input = read_input()
    crabs_counter = Counter(input)
    crabs_positions = list(set(input))
    computed_fuels = Counter()

    for position in range(min(crabs_positions), max(crabs_positions)):
        fuels = []
        for crab_pos, n_crabs in crabs_counter.items():
            distance = abs(crab_pos - position)
            summation = ((distance * distance) + distance) / 2
            fuels.append(n_crabs * summation)
        computed_fuels[position] = sum(fuels)

    return int(computed_fuels.most_common()[-1][1])


write_output(solve_1(), solve_2())
