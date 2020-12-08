import os


def read_instructions():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    instructions = []
    with open(file_path) as f:
        for line in (line.strip() for line in f):
            instructions.append((line[:3], line[4:]))
    return instructions


def solve(instructions):
    accumulator = 0
    instruction_number = 0
    executed_instructions = set()

    while instruction_number not in executed_instructions:
        executed_instructions.add(instruction_number)
        ins, num = instructions[instruction_number]
        if ins == "nop":
            instruction_number += 1
        elif ins == "acc":
            accumulator += int(num)
            instruction_number += 1
        elif ins == "jmp":
            instruction_number += int(num)

    return accumulator


print(solve(read_instructions()))
