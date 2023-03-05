import os
from utils.io import write_output


def read_input():
    rock_obstacles = set()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            blocks = line.strip().split(" -> ")
            for i in range(len(blocks) - 1):
                start = list(map(int, blocks[i].split(",")))
                end = list(map(int, blocks[i + 1].split(",")))
                if start[0] == end[0]:
                    y_coordinates = sorted([start[1], end[1]])
                    for i in range(y_coordinates[0], y_coordinates[1] + 1):
                        rock_obstacles.add((start[0], i))
                else:
                    x_coordinates = sorted([start[0], end[0]])
                    for i in range(x_coordinates[0], x_coordinates[1] + 1):
                        rock_obstacles.add((i, start[1]))
    return rock_obstacles


def drop_sand(obstacles, bottom_limit, has_floor):
    sand_unit_pos = start_position = (500, 0)
    counter = 0

    while True:
        down_pos = (sand_unit_pos[0], sand_unit_pos[1] + 1)
        left_pos = (sand_unit_pos[0] - 1, sand_unit_pos[1] + 1)
        right_pos = (sand_unit_pos[0] + 1, sand_unit_pos[1] + 1)
        if down_pos[1] == bottom_limit:
            if has_floor:
                # add to the floor
                obstacles.add(sand_unit_pos)
                sand_unit_pos = start_position
                counter += 1
            else:
                # endless void reached
                break
        elif down_pos not in obstacles:
            sand_unit_pos = down_pos
        elif left_pos not in obstacles:
            sand_unit_pos = left_pos
        elif right_pos not in obstacles:
            sand_unit_pos = right_pos
        else:
            # cannot move...
            obstacles.add(sand_unit_pos)
            counter += 1
            if sand_unit_pos == start_position:
                break
            sand_unit_pos = start_position

    return counter


def solve_1(rock_units):
    return drop_sand(set(rock_units), max(x[1] for x in rock_units) + 1, False)


def solve_2(rock_units):
    return drop_sand(set(rock_units), max(x[1] for x in rock_units) + 2, True)


input = read_input()
write_output(solve_1(input), solve_2(input))
