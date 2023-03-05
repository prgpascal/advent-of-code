import os
from collections import defaultdict
from utils.io import write_output


ROUND_PRIORITIES = [
    (("N", "NE", "NW"), "N"),
    (("S", "SE", "SW"), "S"),
    (("W", "NW", "SW"), "W"),
    (("E", "NE", "SE"), "E"),
]


def read_input():
    positions = set()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for i, row in enumerate(file):
            for j, cell in enumerate(row.strip()):
                if cell == "#":
                    positions.add((i, j))
    return positions


def get_adjacent_positions(current_position, directions):
    positions = set()
    for direction in directions:
        match direction:
            case "N":
                positions.add((current_position[0] - 1, current_position[1]))
            case "S":
                positions.add((current_position[0] + 1, current_position[1]))
            case "W":
                positions.add((current_position[0], current_position[1] - 1))
            case "E":
                positions.add((current_position[0], current_position[1] + 1))
            case "NE":
                positions.add((current_position[0] - 1, current_position[1] + 1))
            case "NW":
                positions.add((current_position[0] - 1, current_position[1] - 1))
            case "SE":
                positions.add((current_position[0] + 1, current_position[1] + 1))
            case "SW":
                positions.add((current_position[0] + 1, current_position[1] - 1))
    return positions


def solve(positions, max_rounds):
    rotation_index = 0
    for round in range(max_rounds):
        proposed_positions = defaultdict(list)

        for elf_position in positions:
            adj = get_adjacent_positions(
                elf_position, ("N", "S", "W", "E", "NE", "NW", "SE", "SW")
            )
            if len(adj.intersection(positions)) == 0:
                continue

            for rotation in range(rotation_index, rotation_index + 4):
                directions, target = ROUND_PRIORITIES[rotation % len(ROUND_PRIORITIES)]
                adj = get_adjacent_positions(elf_position, directions).intersection(
                    positions
                )
                if not adj:
                    dest = get_adjacent_positions(elf_position, tuple(target)).pop()
                    proposed_positions[dest].append(elf_position)
                    break

        moving_elves = 0
        for k, v in proposed_positions.items():
            if len(v) == 1:
                moving_elves += 1
                positions.add(k)
                positions.remove(v.pop())

        if moving_elves == 0:
            # no elf is moving, return the round number (for part #2)
            return round + 1

        rotation_index += 1

    # max rounds reached, return the number of empty ground tiles (for part #1)
    min_x = max_x = min_y = max_y = 0
    for position in positions:
        min_x = min(min_x, position[0])
        max_x = max(max_x, position[0])
        min_y = min(min_y, position[1])
        max_y = max(max_y, position[1])
    width = len(range(min_x, max_x + 1))
    height = len(range(min_y, max_y + 1))

    return width * height - len(positions)


def solve_1():
    return solve(read_input(), 10)


def solve_2():
    return solve(read_input(), 5000000)


write_output(solve_1(), solve_2())
