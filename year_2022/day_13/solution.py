import os
from functools import cmp_to_key
from utils.io import write_output

NUMBERS_REGEX = r"(\d+)"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip() for line in file.readlines() if line.strip() != ""]


def get_next_substring(string, start_index):
    end_index = start_index
    substring = string[start_index]
    if substring.isnumeric():
        # look for other digits
        while string[end_index + 1].isnumeric():
            end_index += 1
            substring += string[end_index]
    return (substring, end_index)


def are_in_order(left, right):
    left_sub, i = get_next_substring(left, 0)
    right_sub, j = get_next_substring(right, 0)

    if left_sub == right_sub:
        return are_in_order(left[i + 1 :], right[j + 1 :])
    elif left_sub.isnumeric() and right_sub.isnumeric():
        return int(left_sub) < int(right_sub)
    elif left_sub == "]":
        return True
    elif right_sub == "]":
        return False
    elif left_sub == "[":
        return are_in_order(left, f"[{right_sub}]{right[j + 1:]}")
    elif right_sub == "[":
        return are_in_order(f"[{left_sub}]{left[i+ 1:]}", right)

    return False


def custom_compare(pair1, pair2):
    return -1 if are_in_order(pair1, pair2) else 1


def solve_1(input):
    pairs_in_order = []
    pair_number = 0
    for i in range(0, len(input), 2):
        pair_number += 1
        if are_in_order(input[i], input[i + 1]):
            pairs_in_order.append(pair_number)
    return sum(pairs_in_order)


def solve_2(input):
    divider_packets = ["[[2]]", "[[6]]"]
    packets = input + divider_packets
    sorted_packets = sorted(packets, key=cmp_to_key(custom_compare))
    result = 1
    for i, packet in enumerate(sorted_packets, start=1):
        if packet in divider_packets:
            result *= i
    return result


input = read_input()
write_output(solve_1(input), solve_2(input))
