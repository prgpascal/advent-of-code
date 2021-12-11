import os


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = file.readline().strip().split(",")
    return input


def solve(input, last_turn):
    seen = dict()
    turn = 0
    for number in input:
        turn += 1
        seen[int(number)] = turn

    last = 0
    while turn < last_turn - 1:
        turn += 1
        if last in seen:
            previous_position = seen[last]
            seen[last] = turn
            last = turn - previous_position
        else:
            seen[last] = turn
            last = 0

    return last


input = read_input()
print(solve(input, 2020))
print(solve(input, 30000000))
