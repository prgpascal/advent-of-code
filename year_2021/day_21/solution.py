import os
from utils.io import write_output


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


def solve_2():
    input = read_input()
    return ""


write_output(solve_1(), solve_2())
