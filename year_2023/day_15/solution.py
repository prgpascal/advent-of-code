import os
from collections import deque
from dataclasses import dataclass
from utils.io import write_output


@dataclass
class Box:
    occurrences: set
    lenses: deque


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return file.readline().strip().split(",")


def compute_hash(step: str) -> int:
    current = 0
    for char in step:
        ascii = ord(char)
        current += ascii
        current *= 17
        current = current % 256
    return current


def solve_1(input):
    return sum(compute_hash(step) for step in input)


def solve_2(input):
    result = 0
    boxes = [Box(set(), deque()) for _ in range(256)]
    for step in input:
        if "=" in step:
            label, focal_length = step.split("=")
            lens = (label, focal_length)
            box = boxes[compute_hash(label)]
            if label in box.occurrences:
                # replace the previous lens
                for i in range(len(box.lenses)):
                    if box.lenses[i][0] == label:
                        box.lenses[i] = lens
                        break
            else:
                # add the new lens into the box
                box.occurrences.add(label)
                box.lenses.append(lens)
        else:
            label = step.split("-")[0]
            box = boxes[compute_hash(label)]
            if label in box.occurrences:
                # remove the lens from the box
                to_remove_index = 0
                for i in range(len(box.lenses)):
                    if box.lenses[i][0] == label:
                        to_remove_index = i
                        break
                del box.lenses[to_remove_index]
                box.occurrences.remove(label)

    result = 0
    for box_index, box in enumerate(boxes):
        for slot_index, lens in enumerate(box.lenses):
            result += (box_index + 1) * (slot_index + 1) * int(lens[1])

    return result


input = read_input()
write_output(solve_1(input), solve_2(input))
