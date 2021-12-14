import os
from collections import Counter
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = [line.strip() for line in file.readlines()]
    return input


def solve_1():
    input = read_input()
    gamma_rate_array = []

    for i in range(len(input[0])):
        count = Counter(line[i] for line in input)
        gamma_rate_array.append(count.most_common(1)[0][0])

    epsilon_rate_array = ["1" if x == "0" else "0" for x in gamma_rate_array]
    return int("".join(gamma_rate_array), 2) * int("".join(epsilon_rate_array), 2)


def solve_2():
    input = read_input()
    oxygen_generator_array = input.copy()
    co2_scrubber_array = input.copy()

    for i in range(len(input[0])):
        if len(oxygen_generator_array) > 1:
            count = Counter(line[i] for line in oxygen_generator_array)
            bit = "1" if count["1"] >= count["0"] else "0"
            oxygen_generator_array = [x for x in oxygen_generator_array if x[i] == bit]

        if len(co2_scrubber_array) > 1:
            count = Counter(line[i] for line in co2_scrubber_array)
            bit = "0" if count["0"] <= count["1"] else "1"
            co2_scrubber_array = [x for x in co2_scrubber_array if x[i] == bit]

    return int("".join(oxygen_generator_array), 2) * int("".join(co2_scrubber_array), 2)


write_output(solve_1(), solve_2())
