import os
import re


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        file_blocks = file.read().strip().split("\n\n")
        input_rules = dict(
            {
                rule.split(": ")[0]: rule.split(": ")[1]
                for rule in file_blocks[0].split("\n")
            }
        )
        input_messages = file_blocks[1].split("\n")
    return (input_rules, input_messages)


def create_regex(rule_index, rules):
    rule = rules[rule_index]
    regex = f" {rule} "
    while any(char.isdigit() for char in regex):
        for c in regex.strip().split(" "):
            if c.isdigit():
                sub_rule = rules[c]
                new_sub_rule = f"( {sub_rule} )" if "|" in sub_rule else sub_rule
                regex = regex.replace(f" {c} ", f" {new_sub_rule} ")
    return regex.replace('"', "").replace(" ", "")


def solve_1(input_rules, input_messages):
    regex = create_regex("0", input_rules)
    result = [bool(re.fullmatch(regex, message)) for message in input_messages].count(
        True
    )
    return result


def fix_loops(rules):
    rules["8"] = "( 42 )+"
    rules["11"] = "|".join(" 42 " * i + " 31 " * i for i in range(1, 6))


def solve_2(input_rules, input_messages):
    fix_loops(input_rules)
    return solve_1(input_rules, input_messages)


def write_output(output):
    print(output)


input_rules, input_messages = read_input()
output = solve_1(input_rules, input_messages)
write_output(output)

input_rules["8"] = "42 | 42 8"
input_rules["11"] = "42 31 | 42 11 31"
output = solve_2(input_rules, input_messages)
write_output(output)
