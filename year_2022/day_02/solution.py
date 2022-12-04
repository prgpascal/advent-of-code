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
        return 3  # draw
    if SCORES[round.me] == (SCORES[round.opponent] + 1) % 3:
        return 6  # I win
    return 0  # I lose


def solve_1(input):
    scores = [SCORES[round.me] + 1 + calculate_outcome(round) for round in input]
    return sum(scores)


def solve_2(input):
    result = 0
    for round in input:
        if round.me == "X":
            result += 0 + 1 + (SCORES[round.opponent] - 1) % 3  # I lose
        elif round.me == "Y":
            result += 3 + 1 + SCORES[round.opponent]  # draw
        else:
            result += 6 + 1 + (SCORES[round.opponent] + 1) % 3  # I win
    return result


input = read_input()
write_output(solve_1(input), solve_2(input))
