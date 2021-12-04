from collections import namedtuple
import os

Board = namedtuple("Board", ["rows_set", "columns_set"])
Input = namedtuple("Input", ["numbers", "boards"])


def read_input():
    numbers = []
    tmp_boards = []

    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        numbers = [int(n) for n in file.readline().strip().split(",")]
        file.readline()
        current_board = []
        for line in file:
            line = line.strip()
            if line == "":
                tmp_boards.append(current_board)
                current_board = []
            else:
                current_board.append([int(x) for x in line.split(" ") if x != ""])
        tmp_boards.append(current_board)

    return Input(numbers, [create_board(b) for b in tmp_boards])


def create_board(board_values):
    rows_set = [set(row) for row in board_values]
    columns_set = []
    for i in range(0, 5):
        columns_set.append(set(row[i] for row in board_values))

    return Board(rows_set, columns_set)


def apply_new_number_to_board(board, current_number):
    rows_set, columns_set = board

    for set in rows_set:
        set.discard(current_number)

    for set in columns_set:
        set.discard(current_number)


def is_winning_board(board):
    rows_set, columns_set = board
    return 0 in [len(s) for s in rows_set] + [len(s) for s in columns_set]


def compute_solution(winning_board, winning_number):
    rows_set, columns_set = winning_board
    all_numbers_in_board = set()
    for row, col in zip(rows_set, columns_set):
        all_numbers_in_board.update(row, col)

    return sum(all_numbers_in_board) * winning_number


def solve_1(input: Input):
    numbers, boards = input
    for number in numbers:
        for board in boards:
            apply_new_number_to_board(board, number)
            if is_winning_board(board):
                return compute_solution(board, number)


def solve_2(input):
    numbers, boards = input
    all_winning_boards = []
    to_remove = []

    for number in numbers:
        boards = [b for b in boards if b not in to_remove]
        to_remove = []
        for board in boards:
            apply_new_number_to_board(board, number)
            if is_winning_board(board):
                all_winning_boards.append((board, number))
                to_remove.append(board)

    return compute_solution(all_winning_boards[-1][0], all_winning_boards[-1][1])


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
write_output(solve_1(input), solve_2(input))
