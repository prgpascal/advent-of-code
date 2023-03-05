import os
from collections import deque
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip() for line in file.readlines()]


def snafu_to_decimal(number: str) -> int:
    exponent = 0
    addends = []
    for i in range(len(number) - 1, -1, -1):
        digit = number[i]
        if digit.isdecimal():
            pass
        elif digit == "-":
            digit = "-1"
        elif digit == "=":
            digit = "-2"
        addends.append(int(digit) * pow(5, exponent))
        exponent += 1
    return sum(addends)


def decimal_to_base_5(number: int) -> int:
    remainder = ""
    if number >= 1:
        remainder = decimal_to_base_5(number // 5)
    return int(str(remainder) + str(number % 5))


def replace_with_snafu_special_chars(number: str) -> str:
    result = deque(number)
    for i in range(len(number) - 1, -1, -1):
        if not number[i].isdigit():
            # it's a special char, skip
            continue

        match number[i]:
            case "5":
                result[i] = "0"
            case "3":
                result[i] = "="
            case "4":
                result[i] = "-"
            case _:
                continue

        if i == 0:
            result.appendleft("1")
        else:
            result[i - 1] = str(int(result[i - 1]) + 1)

        return replace_with_snafu_special_chars("".join(result))

    return number


def decimal_to_snafu(number: int) -> str:
    return replace_with_snafu_special_chars(str(decimal_to_base_5(number)))


def solve_1(input):
    decimal_numbers = []
    for number in input:
        decimal_numbers.append(snafu_to_decimal(number))
    return decimal_to_snafu(sum(decimal_numbers))


def solve_2(input):
    return "??"


input = read_input()
write_output(solve_1(input), solve_2(input))
