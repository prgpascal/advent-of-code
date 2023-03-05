import os
from utils.io import write_output


def read_input():
    numbers = []
    zero_item = None
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for i, line in enumerate(file):
            number = int(line.strip())
            numbers.append((number, i))
            if number == 0:
                zero_item = (0, i)
    return (numbers, zero_item)


def execute_mixing(numbers, initial_numbers_list):
    for number in initial_numbers_list:
        start_index = numbers.index(number)
        numbers.pop(start_index)
        end_index = (start_index + number[0]) % len(numbers)
        numbers.insert(end_index, number)


def solve_1(input):
    initial_numbers_list, zero_item = input
    numbers = initial_numbers_list.copy()

    execute_mixing(numbers, initial_numbers_list)

    zero_index = numbers.index(zero_item)
    return (
        numbers[(zero_index + 1000) % len(numbers)][0]
        + numbers[(zero_index + 2000) % len(numbers)][0]
        + numbers[(zero_index + 3000) % len(numbers)][0]
    )


def solve_2(input):
    initial_input, zero_item = input
    initial_input = [(x[0] * 811589153, x[1]) for x in initial_input]
    numbers = initial_input.copy()

    for _ in range(10):
        execute_mixing(numbers, initial_input)

    zero_index = numbers.index(zero_item)
    return (
        numbers[(zero_index + 1000) % len(numbers)][0]
        + numbers[(zero_index + 2000) % len(numbers)][0]
        + numbers[(zero_index + 3000) % len(numbers)][0]
    )


input = read_input()
write_output(solve_1(input), solve_2(input))
