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


def solve_with_variant(instructions, variant_instruction=None):
    Solution = namedtuple(
        'Solution',
        ['accumulator',
         'seen_variants',
         'terminated']
    )

    accumulator = instruction_number = 0
    executed_instructions = set()
    seen_variants = []
    terminated = False

    while (instruction_number not in executed_instructions and
           len(executed_instructions) != len(instructions)):

        if instruction_number == len(instructions):
            terminated = True
            break

        executed_instructions.add(instruction_number)
        ins, num = instructions[instruction_number]

        if instruction_number == variant_instruction:
            ins = "nop" if ins == "jmp" else "jmp"

        if ins == "nop":
            seen_variants.append(instruction_number)
            instruction_number += 1
        elif ins == "acc":
            accumulator += int(num)
            instruction_number += 1
        elif ins == "jmp":
            seen_variants.append(instruction_number)
            instruction_number += int(num)

    return Solution(
        accumulator=accumulator,
        seen_variants=seen_variants,
        terminated=terminated
    )


def solve(instructions):
    solution = solve_with_variant(instructions)
    variants = solution.seen_variants
    while not solution.terminated:
        if len(variants) > 0:
            solution = solve_with_variant(
                instructions, 
                variant_instruction=variants.pop())
            
    return solution.accumulator


print(solve(read_instructions()))
