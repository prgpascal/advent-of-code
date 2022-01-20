import os
from utils.io import write_output

# Solved with the help of the Reddit community. This exercise was so challenging (>_<)"
# Credit:
# - https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hpuu3e0/?utm_source=share&utm_medium=web2x&context=3
# - https://topaz.github.io/paste/#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


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input_lines = [line.strip() for line in file.readlines()]
        instructions = [line.split() for line in input_lines]
        return instructions


class ALU:
    def __init__(self, cmds):
        self.cmds = cmds
        self.reg = {"w": 0, "x": 0, "y": 0, "z": 0}

    def get_param_value(self, param):
        return self.reg[param] if param in self.reg else int(param)

    def check_solution(self, input):
        inputs = iter(input)
        self.reg = {"w": 0, "x": 0, "y": 0, "z": 0}

        for operator, *params in self.cmds:
            if operator == "inp":
                self.reg[params[0]] = next(inputs)
            elif operator == "add":
                self.reg[params[0]] += self.get_param_value(params[1])
            elif operator == "mul":
                self.reg[params[0]] *= self.get_param_value(params[1])
            elif operator == "div":
                self.reg[params[0]] //= self.get_param_value(params[1])
            elif operator == "mod":
                self.reg[params[0]] %= self.get_param_value(params[1])
            elif operator == "eql":
                first = self.get_param_value(params[0])
                second = self.get_param_value(params[1])
                self.reg[params[0]] = int(first == second)

        return self.reg.copy()


def adjust_input(input, cmds):
    sub_len = 18  # length of the subroutine for each of the inputs.
    line_numbers = [4, 5, 15]  # line numbers with the (div, chk, add) parameters.
    stack = []
    for i in range(14):
        div, chk, add = map(int, [cmds[i * sub_len + x][-1] for x in line_numbers])
        if div == 1:
            stack.append((i, add))
        elif div == 26:
            j, add = stack.pop()
            # Set the input so that the test passes
            input[i] = input[j] + add + chk
            # Adjust the input so that 1 <= inp <= 9
            if input[i] > 9:
                input[j] = input[j] - (input[i] - 9)
                input[i] = 9
            if input[i] < 1:
                input[j] = input[j] + (1 - input[i])
                input[i] = 1

    return input


def solve_for_input(starting_input, cmds):
    inp = adjust_input(starting_input, cmds)
    return "".join(map(str, inp))


def solve_1():
    return solve_for_input([9] * 14, read_input())


def solve_2():
    return solve_for_input([1] * 14, read_input())


write_output(solve_1(), solve_2())
