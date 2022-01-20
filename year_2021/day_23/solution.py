import os
import re
from collections import namedtuple
from utils.io import write_output
from math import inf

Step = namedtuple("Step", ["b1", "b2", "b3", "b4", "spaces", "score"])

INPUT_REGEX = r"#+([^#])#([^#])#([^#])#([^#])#+"
POINTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
BUCKET_CHAR = {0: "A", 1: "B", 2: "C", 3: "D"}
BUCKET_INDEX = {"A": 0, "B": 1, "C": 2, "D": 3}


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        file.readline()
        file.readline()
        b1 = []
        b2 = []
        b3 = []
        b4 = []
        for line in file:
            for match in re.finditer(INPUT_REGEX, line.strip()):
                b1.append(match.group(1))
                b2.append(match.group(2))
                b3.append(match.group(3))
                b4.append(match.group(4))
        return Step(tuple(b1), tuple(b2), tuple(b3), tuple(b4), "." * 11, 0)


def is_bucket_full(bucket, char):
    for x in bucket:
        if x != char:
            return False
    return True


def can_push_into_bucket(step, bucket_position):
    bucket = step[bucket_position]
    char = BUCKET_CHAR[bucket_position]

    if is_bucket_full(bucket, char):
        return False

    for x in bucket:
        if x not in [char, None]:
            return False

    return True


def is_step_finished(step):
    for i in range(0, 4):
        if not is_bucket_full(step[i], BUCKET_CHAR[i]):
            return False
    return True


def is_bucket_empty(bucket):
    return "A" in bucket or "B" in bucket or "C" in bucket or "D" in bucket


def can_pop_from_bucket(step, bucket_position):
    if is_bucket_full(step[bucket_position], BUCKET_CHAR[bucket_position]):
        return False

    return not can_push_into_bucket(step, bucket_position)


def can_place_char_into_index(i):
    return i < 2 or i > 8 or i % 2 == 1


def create_step(old_step, new_bucket, bucket_position, spaces, score):
    old_bucket = list(old_step)
    old_bucket[bucket_position] = tuple(new_bucket)
    return Step(
        old_bucket[0], old_bucket[1], old_bucket[2], old_bucket[3], spaces, score
    )


def get_position_of_item_to_pop(bucket):
    i = 0
    for x in bucket:
        if x is not None:
            break
        i += 1
    return i


def can_pop_and_push(spaces, from_index, to_index):
    for i in range(min(from_index, to_index), max(from_index, to_index) + 1):
        if spaces[i] != ".":
            return False
    return True


def push_items_into_buckets(step):
    result = set()
    for bucket_position in range(0, 4):
        bucket = step[bucket_position]
        char = BUCKET_CHAR[bucket_position]

        if can_push_into_bucket(step, bucket_position):
            start_index = 2 * (bucket_position + 1)

            for my_range in [(start_index, -1, -1), (start_index, len(step.spaces), 1)]:
                new_bucket = list(bucket)
                moves = pos_to_insert = bucket.index(None)
                new_spaces = list(step.spaces)

                for i in range(my_range[0], my_range[1], my_range[2]):
                    moves += 1

                    if new_spaces[i] == ".":
                        continue

                    if new_spaces[i] != char:
                        break

                    # push the item into bucket
                    new_spaces[i] = "."
                    new_bucket[pos_to_insert] = char
                    result.add(
                        create_step(
                            step,
                            new_bucket,
                            bucket_position,
                            "".join(new_spaces),
                            step.score + (moves * POINTS[char]),
                        )
                    )
                    break

    return result


def pop_items_from_buckets(step):
    result = set()
    for bucket_position in range(0, 4):
        if can_pop_from_bucket(step, bucket_position):
            bucket = step[bucket_position]
            start_index = 2 * (bucket_position + 1)

            # Try to pop an item that could be pushed directly into a bucket
            pos_to_remove = get_position_of_item_to_pop(bucket)
            char_to_remove = bucket[pos_to_remove]
            if can_push_into_bucket(step, BUCKET_INDEX[char_to_remove]):
                end_index = 2 * (BUCKET_INDEX[char_to_remove] + 1)
                if can_pop_and_push(step.spaces, start_index, end_index):
                    new_spaces = list(step.spaces)
                    new_bucket = list(bucket)
                    end_index = (
                        end_index + 1 if start_index > end_index else end_index - 1
                    )
                    moves = pos_to_remove + abs(start_index - end_index) + 1

                    # pop the item
                    new_spaces[end_index] = new_bucket[pos_to_remove]
                    new_bucket[pos_to_remove] = None
                    result.add(
                        create_step(
                            step,
                            new_bucket,
                            bucket_position,
                            "".join(new_spaces),
                            step.score + (moves * POINTS[new_spaces[end_index]]),
                        )
                    )
                    continue

            for my_range in [(start_index, -1, -1), (start_index, len(step.spaces), 1)]:
                new_bucket = list(bucket)
                pos_to_remove = moves = get_position_of_item_to_pop(bucket)

                for i in range(my_range[0], my_range[1], my_range[2]):
                    new_bucket = list(bucket)
                    moves += 1
                    if not can_place_char_into_index(i):
                        continue

                    new_spaces = list(step.spaces)
                    if new_spaces[i] != ".":
                        break
                    else:
                        # pop the item
                        new_spaces[i] = new_bucket[pos_to_remove]
                        new_bucket[pos_to_remove] = None
                        new_step = create_step(
                            step,
                            new_bucket,
                            bucket_position,
                            "".join(new_spaces),
                            step.score + (moves * POINTS[new_spaces[i]]),
                        )
                        if not is_invalid_step(new_step):
                            result.add(new_step)

    return result


def is_invalid_step(step):
    spaces = step.spaces
    if (
        (spaces[3] == "C" and spaces[7] == "A")
        or (spaces[3] == "D" and spaces[7] == "A")
        or (spaces[3] == "C" and spaces[7] == "B")
        or (spaces[3] == "D" and spaces[7] == "B")
        or (spaces[3] == "C" and spaces[5] == "A")
        or (spaces[3] == "D" and spaces[5] == "A")
        or (spaces[5] == "D" and spaces[7] == "A")
        or (spaces[5] == "D" and spaces[7] == "B")
    ):
        return True
    return False


def solve(first_step):
    steps = set()
    steps.add(first_step)
    minimum = inf
    while steps:
        step = steps.pop()
        if step.score >= minimum:
            continue

        if is_step_finished(step):
            minimum = min(step.score, minimum)
            continue

        new_inserted_items = push_items_into_buckets(step)
        steps.update(new_inserted_items)
        if not new_inserted_items:
            steps.update(pop_items_from_buckets(step))

    return minimum


def solve_1():
    first_step = read_input()
    return solve(first_step)


def solve_2():
    r1, r2, r3, r4, spaces, score = read_input()
    new_step = Step(
        tuple([r1[0], "D", "D", r1[1]]),
        tuple([r2[0], "C", "B", r2[1]]),
        tuple([r3[0], "B", "A", r3[1]]),
        tuple([r4[0], "A", "C", r4[1]]),
        spaces,
        score,
    )
    return solve(new_step)


write_output(solve_1(), solve_2())
