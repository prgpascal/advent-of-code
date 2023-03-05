import os
import re
from collections import defaultdict, namedtuple, deque
from utils.io import write_output

INSTRUCTION_REGEX = r"move (\d+) from (\d+) to (\d+)"
Instruction = namedtuple("Instruction", ["quantity", "source", "target"])


def read_input():
    stacks = defaultdict(list)
    instructions = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            if match := re.search(INSTRUCTION_REGEX, line):
                instructions.append(
                    Instruction(
                        quantity=int(match.group(1)),
                        source=int(match.group(2)),
                        target=int(match.group(3)),
                    )
                )
            else:
                for i, char in enumerate(line):
                    if char.isalpha():
                        stack_number = ((i - 1) // 4) + 1
                        stacks[stack_number].insert(0, char)
    return (stacks, instructions)


def solve_1():
    stacks, instructions = read_input()
    for instruction in instructions:
        quantity, source, target = instruction
        for _ in range(quantity):
            stacks[target].append(stacks[source].pop())

    return "".join([stacks[i + 1][-1] for i in range(len(stacks))])


def solve_2():
    stacks, instructions = read_input()
    for instruction in instructions:
        quantity, source, target = instruction
        temp_stack = deque()
        for _ in range(quantity):
            temp_stack.appendleft(stacks[source].pop())
        stacks[target].extend(temp_stack)

    return "".join([stacks[i + 1][-1] for i in range(len(stacks))])


write_output(solve_1(), solve_2())
