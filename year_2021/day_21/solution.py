from collections import namedtuple
import os
from utils.io import write_output
from itertools import product
from functools import lru_cache

Universe = namedtuple("Universe", ("pos1", "score1", "pos2", "score2"))
TARGET_SCORE = 21


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        player_1_position = int(file.readline().strip()[-1])
        player_2_position = int(file.readline().strip()[-1])
        return (player_1_position, player_2_position)


def solve_1():
    player_1_position, player_2_position = read_input()
    last_roll = i = player_1_score = player_2_score = 0
    turn_player_one = True

    while True:
        i += 1
        new_roll = (last_roll + 1) + (last_roll + 2) + (last_roll + 3)
        if turn_player_one:
            new_position = (player_1_position + new_roll) % 10
            new_position = new_position if new_position > 0 else 10
            player_1_position = new_position
            player_1_score += new_position
        else:
            new_position = (player_2_position + new_roll) % 10
            new_position = new_position if new_position > 0 else 10
            player_2_position = new_position
            player_2_score += new_position

        last_roll += 3
        turn_player_one = not turn_player_one

        if player_1_score >= 1000 or player_2_score >= 1000:
            break

    return min(player_1_score, player_2_score) * (i * 3)


def do_move(position, score, dices_sum):
    new_position = (position + dices_sum) % 10
    new_position = new_position if new_position > 0 else 10
    new_score = score + new_position
    return new_position, new_score


@lru_cache(maxsize=None)
def recursive_count_victories(player_turn, universe):
    pos1, score1, pos2, score2 = universe

    if score1 >= TARGET_SCORE:
        return 1, 0  # player 1 wins
    elif score2 >= TARGET_SCORE:
        return 0, 1  # player 2 wins

    victories = [0, 0]
    for dices in product(range(1, 4), repeat=3):
        if player_turn == 1:
            new_pos, new_score = do_move(pos1, score1, sum(dices))
            new_universe = Universe(new_pos, new_score, pos2, score2)
            victories1, victories2 = recursive_count_victories(2, new_universe)
        else:
            new_pos, new_score = do_move(pos2, score2, sum(dices))
            new_universe = Universe(pos1, score1, new_pos, new_score)
            victories1, victories2 = recursive_count_victories(1, new_universe)

        victories[0] += victories1
        victories[1] += victories2

    return victories[0], victories[1]


def solve_2():
    initial_position = read_input()
    starting_universe = Universe(initial_position[0], 0, initial_position[1], 0)
    victories = recursive_count_victories(0, starting_universe)
    return max(victories)


write_output(solve_1(), solve_2())
