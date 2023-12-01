import os
from dataclasses import dataclass
from utils.io import write_output
from utils.utils import INFINITY

STRING_DIGITS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
INT_DIGITS = [str(x) for x in range(1, 10)]
ALL_DIGITS = STRING_DIGITS + INT_DIGITS


@dataclass(frozen=True)
class MyDigit:
    value: str
    position: float

    def to_int(self) -> int:
        return (
            int(self.value)
            if self.value.isdigit()
            else STRING_DIGITS.index(self.value) + 1
        )


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip() for line in file.readlines()]


def solve_1(input):
    calibration_values_sum = 0
    for line in input:
        numbers = [int(x) for x in line if x.isdigit()]
        calibration_values_sum += numbers[0] * 10 + numbers[-1]
    return calibration_values_sum


def solve_2(input):
    calibration_values_sum = 0
    for line in input:
        first_digit = MyDigit("", INFINITY)
        last_digit = MyDigit("", -1)

        for n in ALL_DIGITS:
            if n in line:
                first_index = line.index(n)
                if first_index < first_digit.position:
                    first_digit = MyDigit(n, first_index)

                last_index = line.rindex(n)
                if last_index > last_digit.position:
                    last_digit = MyDigit(n, last_index)

        calibration_values_sum += first_digit.to_int() * 10 + last_digit.to_int()

    return calibration_values_sum


input = read_input()
write_output(solve_1(input), solve_2(input))
