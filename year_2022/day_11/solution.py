import os
import re
from functools import reduce
from utils.io import write_output

REGEX_ID = r"Monkey (\d+)"
STARTING_REGEX = r"(\d+)"
OPERATION_REGEX = r"Operation: new = (\S+) (.) (\S+)"
TEST_REGEX = r"Test: divisible by (\d*)"
TRUE_REGEX = r"If true:(.*)(\d+)"
FALSE_REGEX = r"If false:(.*)(\d+)"


# Solved with the help of the Reddit community. This exercise was so challenging (>_<)"


class Monkey:
    def __init__(
        self, monkey_id, starting_items, operation, test, true_out, false_out, monkeys
    ):
        self.monkey_id = monkey_id
        self.starting_items = starting_items
        self.operation = operation
        self.test = test
        self.true_out = true_out
        self.false_out = false_out
        self.monkeys = monkeys
        self.inspected = 0

    def perform_turn(self, part_2_module=None):
        for item in self.starting_items:
            worry_level = self.operation(item)

            if part_2_module is None:
                worry_level = worry_level // 3
            else:
                worry_level = worry_level % part_2_module

            target = None
            if worry_level % self.test == 0:
                target = self.monkeys[self.true_out]
            else:
                target = self.monkeys[self.false_out]
            target.starting_items.append(worry_level)

        self.inspected += len(self.starting_items)
        self.starting_items = []


def read_input():
    input = dict()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        monkey_id = None
        starting = []
        operation = None
        test = None
        true_out = None
        false_out = None

        for line in file:
            line = line.strip()
            if match := re.search(REGEX_ID, line):
                monkey_id = int(match.group(1))
            elif line.startswith("Starting"):
                if starting_match := re.findall(STARTING_REGEX, line):
                    starting = [int(x) for x in starting_match]
            elif match := re.search(OPERATION_REGEX, line):
                operation = match.group(2)
                target = match.group(3)
                match operation:
                    case "*":
                        # https://stackoverflow.com/a/7546960/2762461
                        operation = lambda x, t=target: x * (
                            int(t) if t != "old" else x
                        )
                    case "+":
                        operation = lambda x, t=target: x + (
                            int(t) if t != "old" else x
                        )
            elif match := re.search(TEST_REGEX, line):
                test = int(match.group(1))
            elif match := re.search(TRUE_REGEX, line):
                true_out = int(match.group(2))
            elif match := re.search(FALSE_REGEX, line):
                false_out = int(match.group(2))
            else:
                input[monkey_id] = Monkey(
                    monkey_id, starting, operation, test, true_out, false_out, input
                )
        input[monkey_id] = Monkey(
            monkey_id, starting, operation, test, true_out, false_out, input
        )
    return input


def solve_1():
    monkeys = read_input()
    for _ in range(20):
        for monkey in monkeys.values():
            monkey.perform_turn()
    most_inspected = sorted([x.inspected for x in monkeys.values()])[-2:]
    return reduce(lambda x, y: x * y, most_inspected)


def solve_2():
    monkeys = read_input()

    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    mod_all = 1
    for div_by in [m.test for m in monkeys.values()]:
        mod_all *= div_by

    for _ in range(10000):
        for monkey in monkeys.values():
            monkey.perform_turn(mod_all)
    most_inspected = sorted([x.inspected for x in monkeys.values()])[-2:]
    return reduce(lambda x, y: x * y, most_inspected)


write_output(solve_1(), solve_2())
