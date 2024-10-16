import os
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            input.append([int(x) for x in line.strip().split(" ")])
        return input


def solve(input):
    results = []
    for history in input:
        matrix = [history]
        all_zeros = False
        while not all_zeros:
            all_zeros = True
            new_history = []
            last_history = matrix[-1]
            for i in range(len(last_history) - 1):
                new_history.append(last_history[i + 1] - last_history[i])
                if new_history[-1] != 0:
                    all_zeros = False
            matrix.append(new_history)

        for i in range(len(matrix) - 2, -1, -1):
            # add last history value
            matrix[i].append(matrix[i][-1] + matrix[i + 1][-1])

        # pick the desired history value
        results.append(matrix[0][-1])

    return sum(results)


def solve_1(input):
    return solve(input)


def solve_2(input):
    reversed_input = [list(reversed(x)) for x in input]
    return solve(reversed_input)


write_output(solve_1(read_input()), solve_2(read_input()))
