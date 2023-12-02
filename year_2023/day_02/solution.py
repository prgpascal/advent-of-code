import os
import re
from collections import defaultdict
from utils.io import write_output
from math import prod

CUBES = {"red": 12, "green": 13, "blue": 14}


def read_input():
    games = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            game_id, sets = line.strip().split(":")
            game_id = int(game_id.split(" ")[1])
            games.append((game_id, sets))
    return games


def solve_1(input):
    impossible_games_ids = set()
    for game_id, sets in input:
        for color, max_n in CUBES.items():
            for match in re.finditer(f"\s(\d+) {color}", sets):
                n = int(match.group(1))
                if n > max_n:
                    impossible_games_ids.add(game_id)

    all_games_ids = set(range(1, len(input) + 1))
    return sum(all_games_ids - impossible_games_ids)


def solve_2(input):
    sets_powers = []
    for _, sets in input:
        found = defaultdict(lambda: -1)
        for color in CUBES.keys():
            for match in re.finditer(f"\s(\d+) {color}", sets):
                n = int(match.group(1))
                found[color] = max(found[color], n)
        sets_powers.append(prod(v for v in found.values()))

    return sum(sets_powers)


input = read_input()
write_output(solve_1(input), solve_2(input))
