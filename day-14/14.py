import os
import re

MASK_REGEX = r"mask = (\w+)"
INSTRUCTION_REGEX = r"mem\[(\d+)] = (\d+)"


def read_input():
    file_path = os.path.join(os.path.dirname(__file__), "input.txt")
    instructions_set = []
    mask = ""
    instructions_list = []
    with open(file_path) as f:
        for line in f:
            if line.startswith("mask"):
                for match in re.finditer(MASK_REGEX, line.strip()):
                    if mask != "":
                        instructions_set.append(
                            {"mask": mask, "instructions": list(instructions_list)}
                        )
                        instructions_list = []
                    mask = match.group(1)
            else:
                for match in re.finditer(INSTRUCTION_REGEX, line.strip()):
                    instructions_list.append((match.group(1), match.group(2)))

    instructions_set.append({"mask": mask, "instructions": list(instructions_list)})
    return instructions_set


def set_bit_value(number, bit_position, bit_value):
    if bit_value == 1:
        return number | (1 << bit_position)
    return number & ~(1 << bit_position)


def apply_instruction_problem_1(mem_dict, instruction, mask):
    value = int(instruction[1])
    for i, m in enumerate(reversed(mask)):
        if m != "X":
            value = set_bit_value(value, i, int(m))
    mem_dict[instruction[0]] = value


def apply_instruction_problem_2(mem_dict, instruction, mask):
    mem_addresses = set()
    mem_addresses.add(int(instruction[0]))
    for i, m in enumerate(reversed(mask)):
        tmp_addresses = set()
        while len(mem_addresses) > 0:
            value = mem_addresses.pop()
            if m == "1":
                tmp_addresses.add(set_bit_value(value, i, 1))
            elif m == "X":
                tmp_addresses.add(set_bit_value(value, i, 0))
                tmp_addresses.add(set_bit_value(value, i, 1))
            else:
                tmp_addresses.add(value)
        mem_addresses = set(tmp_addresses)

    for address in mem_addresses:
        mem_dict[address] = int(instruction[1])


def solve_problem_1(instructions_set):
    mem_dict = {}
    for instruction_s in instructions_set:
        mask = instruction_s["mask"]
        instructions = instruction_s["instructions"]
        for ins in instructions:
            apply_instruction_problem_1(mem_dict, ins, mask)
    return sum(mem_dict.values())


def solve_problem_2(instructions_set):
    mem_dict = {}
    for instruction_s in instructions_set:
        mask = instruction_s["mask"]
        instructions = instruction_s["instructions"]
        for ins in instructions:
            apply_instruction_problem_2(mem_dict, ins, mask)
    return sum(mem_dict.values())


input = read_input()
print("SOLUTION 1: " + str(solve_problem_1(input)))
print("SOLUTION 2: " + str(solve_problem_2(input)))
