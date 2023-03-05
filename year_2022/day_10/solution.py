import os
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip().split(" ") for line in file.readlines()]


def update_signal_strengths(cycle, register_value, signal_strengths):
    interesting_cycles = (20, 60, 100, 140, 180, 220)
    current_cycle = cycle + 1
    if current_cycle in interesting_cycles:
        signal_strengths[current_cycle] = current_cycle * register_value


def get_pixel_char(cycle, sprite_position):
    return (
        "#"
        if cycle % 40 in (sprite_position - 1, sprite_position, sprite_position + 1)
        else " "
    )


def solve_1(input):
    register_value = 1
    ended_cycles = 0
    signal_strengths = dict()

    for instruction in input:
        update_signal_strengths(ended_cycles, register_value, signal_strengths)
        if len(instruction) > 1:
            ended_cycles += 1
            update_signal_strengths(ended_cycles, register_value, signal_strengths)
            register_value += int(instruction[1])
        ended_cycles += 1

    return sum([strength for strength in signal_strengths.values()])


def solve_2(input):
    sprite_position = 1
    ended_cycles = 0
    row = ""
    for instruction in input:
        row += get_pixel_char(ended_cycles, sprite_position)
        if len(instruction) > 1:
            ended_cycles += 1
            row += get_pixel_char(ended_cycles, sprite_position)
            sprite_position += int(instruction[1])
        ended_cycles += 1

    result = ""
    for i in range(0, 201, 40):
        result += row[i:i+40]
        result += "\n"

    return result


input = read_input()
write_output(solve_1(input), solve_2(input))
