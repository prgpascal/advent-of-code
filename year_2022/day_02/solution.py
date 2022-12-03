import os
from collections import namedtuple

from utils.io import write_output

Round = namedtuple("Round", ["opponent", "me"])

SCORES = {
    "A": 0,  # rock
    "B": 1,  # paper
    "C": 2,  # scissors
    "X": 0,  # rock / lose
    "Y": 1,  # paper / draw
    "Z": 2,  # scissors / win
}


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            round = line.strip().split(" ")
            input.append(Round(round[0], round[1]))
    return input


def calculate_outcome(round):
    if SCORES[round.opponent] == SCORES[round.me]:
        # draw
        return 3

    if SCORES[round.me] == (SCORES[round.opponent] + 1) % 3:
        # I win
        return 6

    return 0  # I lose


def solve_1():
    input = read_input()
    result = 0
    for round in input:
        result += SCORES[round.me] + 1 + calculate_outcome(round)
    return result


def solve_2():
    input = read_input()
    result = 0
    for round in input:
        if round.me == "X":
            # I lose
            result += 0 + 1 + (SCORES[round.opponent] - 1) % 3
        elif round.me == "Y":
            # draw
            result += 3 + 1 + SCORES[round.opponent]
        else:
            # I win
            result += 6 + 1 + (SCORES[round.opponent] + 1) % 3

    return result


write_output(solve_1(), solve_2())
