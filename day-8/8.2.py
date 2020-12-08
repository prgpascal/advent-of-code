import os
from collections import namedtuple


def read_instructions():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    instructions = []
    with open(file_path) as f:
        for line in (line.strip() for line in f):
            instructions.append((line[:3], line[4:]))
    return instructions


def solve_with_variant(instructions, variant_jmp_instruction=None, variant_nop_instruction=None):
    Solution = namedtuple(
        'Solution',
        ['accumulator',
         'seen_jmp_instructions',
         'seen_nop_instructions',
         'terminated']
    )

    accumulator = instruction_number = 0
    executed_instructions = set()
    seen_jmp_instructions = []
    seen_nop_instructions = []
    terminated = False

    while (instruction_number not in executed_instructions and
           len(executed_instructions) != len(instructions)):

        if instruction_number == len(instructions):
            terminated = True
            break

        executed_instructions.add(instruction_number)
        ins, num = instructions[instruction_number]

        if instruction_number == variant_jmp_instruction:
            ins = "nop"
        elif instruction_number == variant_nop_instruction:
            ins = "jmp"

        if ins == "nop":
            seen_nop_instructions.append(instruction_number)
            instruction_number += 1
        elif ins == "acc":
            accumulator += int(num)
            instruction_number += 1
        elif ins == "jmp":
            seen_jmp_instructions.append(instruction_number)
            instruction_number += int(num)

    return Solution(
        accumulator=accumulator,
        seen_jmp_instructions=seen_jmp_instructions,
        seen_nop_instructions=seen_nop_instructions,
        terminated=terminated
    )


def solve(instructions):
    solution = solve_with_variant(instructions)
    seen_jmp_instructions = solution.seen_jmp_instructions
    seen_nop_instructions = solution.seen_nop_instructions

    while not solution.terminated:
        if len(seen_jmp_instructions) > 0:
            jmp_variant = seen_jmp_instructions.pop()
            solution = solve_with_variant(
                instructions, variant_jmp_instruction=jmp_variant)
        elif len(seen_nop_instructions) > 0:
            nop_variant = seen_nop_instructions.pop()
            solution = solve_with_variant(
                instructions, variant_nop_instruction=nop_variant)

    return solution.accumulator


print(solve(read_instructions()))
