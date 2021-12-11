import os
from collections import deque

operators = ("*", "+")


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = [line.strip() for line in file.readlines()]
    return input


def recursive_calculator(my_deque):
    last_number = 0
    last_operator = ""
    number_string = ""

    while len(my_deque) > 0:
        char = my_deque.popleft()

        if char == " ":
            continue

        if char.isdigit():
            number_string += char

        if char == "(":
            recursive_value = recursive_calculator(my_deque)
            number_string = str(recursive_value)

        if len(my_deque) == 0 or char in operators or char == ")":
            number = int(number_string)
            if last_operator == "*":
                number = last_number * number
            elif last_operator == "+":
                number = last_number + number

            last_number = number
            last_operator = char
            number_string = ""

        if char == ")":
            break

    return last_number


def solve(input):
    results = []
    for expression in input:
        results.append(recursive_calculator(deque(list(expression))))
    return sum(results)


def write_output(output):
    print(output)


input = read_input()
output = solve(input)
write_output(output)
