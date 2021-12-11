import os


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [int(x) for x in file.readline().strip().split(",")]


def solve_for_day(input, day):
    fishes_list = input.copy()
    fishes_per_timer = [0] * 9
    for fish in fishes_list:
        fishes_per_timer[fish] += 1

    for _ in range(day):
        number_of_new_fishes = fishes_per_timer[0]
        for index in range(1, 9):
            fishes_per_timer[index - 1] = fishes_per_timer[index]
        fishes_per_timer[6] += number_of_new_fishes
        fishes_per_timer[8] = number_of_new_fishes

    return sum(fishes_per_timer)


def solve_1(input):
    return solve_for_day(input, 80)


def solve_2(input):
    return solve_for_day(input, 256)


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
write_output(solve_1(input), solve_2(input))
