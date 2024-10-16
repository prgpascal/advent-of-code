from functools import lru_cache
import os
import re
from dataclasses import dataclass
from utils.io import write_output

INVERSE_OPERATORS = {"<=": ">", ">=": "<", ">": "<=", "<": ">="}


@dataclass
class Workflow:
    rules: list[str]
    default: str


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        workflows = dict()
        ratings = []
        read_workflows = True
        for line in file:
            line = line.strip()
            if line == "":
                read_workflows = False
            if read_workflows:
                if match := re.search(r"(.*){(.*)}", line):
                    id, rules = match.groups()
                    all_rules = rules.split(",")
                    default = all_rules[-1]
                    rules = [r for r in all_rules[0:-1]]
                    workflows[id] = Workflow(rules, default)
            else:
                if match := re.search(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", line):
                    x, m, a, s = [int(x) for x in match.groups()]
                    ratings.append({"x": x, "m": m, "a": a, "s": s})
        return (workflows, ratings)


@lru_cache()
def extract_rule(rule: str):
    if match := re.search(r"(.*)([<>][=]?)(\d*):(.*)", rule):
        prop, symbol, number, target = match.groups()
        return (prop, symbol, int(number), target)
    raise Exception("Rule malformed", rule)


def solve_1(input):
    workflows, ratings = input
    results = []
    for rating in ratings:
        work_id = "in"
        while work_id not in ["R", "A"]:
            work = workflows[work_id]
            rule_matched = False
            for rule in work.rules:
                prop, symbol, number, target = extract_rule(rule)
                if symbol == ">":
                    if rating[prop] > number:
                        work_id = target
                        rule_matched = True
                        break
                else:
                    if rating[prop] < number:
                        work_id = target
                        rule_matched = True
                        break

            if not rule_matched:
                work_id = work.default

            if work_id == "A":
                results.append((work_id, rating))

    return sum([sum(r[1].values()) for r in results])


def invert_rule(rule: str):
    for k, v in INVERSE_OPERATORS.items():
        if k in rule:
            return rule.replace(k, v).split(":")[0]
    raise Exception("Rule malformed", rule)


def rewrite_rules_part_2(work: Workflow):
    new_rules = []
    for i, rule in enumerate(work.rules):
        new_sub_rules = ""
        for j in range(i):
            # reverse previous rules to make this rule true
            new_sub_rules += str(invert_rule(work.rules[j])) + ","
        new_sub_rules += str(rule)
        new_rules.append(new_sub_rules)

    # add the default rule
    new_sub_rules = ""
    for rule in work.rules:
        new_sub_rules += str(invert_rule(rule)) + ","
    new_sub_rules += f"x>0:{work.default}"
    new_rules.append(new_sub_rules)

    work.rules = new_rules


def expand_rules_recursively(work, workflows):
    new_rules = []
    for rules in work.rules:
        if rules.endswith("A"):
            new_rules.append(rules)
            pass
        elif rules.endswith("R"):
            # not interested in rejection rules
            pass
        else:
            prev_rule, target = rules.split(":")
            expand_rules_recursively(workflows[target], workflows)
            target_rules = workflows[target].rules
            new_rules.extend([f"{prev_rule},{t}" for t in target_rules])
    work.rules = new_rules


def solve_2(input):
    workflows, _ = input

    for w in workflows.values():
        rewrite_rules_part_2(w)

    expand_rules_recursively(workflows["in"], workflows)

    MIN_VALUE = 1
    MAX_VALUE = 4000
    results = []
    for rule in workflows["in"].rules:
        ranges = {
            "x": (MIN_VALUE, MAX_VALUE),
            "m": (MIN_VALUE, MAX_VALUE),
            "a": (MIN_VALUE, MAX_VALUE),
            "s": (MIN_VALUE, MAX_VALUE),
        }
        for subrule in rule.split(":")[0].split(","):
            if ">=" in subrule:
                item, number = subrule.split(">=")
                prev = ranges[item]
                if prev[0] < int(number):
                    ranges[item] = (int(number), prev[1])
            elif "<=" in subrule:
                item, number = subrule.split("<=")
                prev = ranges[item]
                if prev[1] > int(number):
                    ranges[item] = (prev[0], int(number))
            elif ">" in subrule:
                item, number = subrule.split(">")
                prev = ranges[item]
                if prev[0] <= int(number):
                    ranges[item] = (int(number) + 1, prev[1])
            elif "<" in subrule:
                item, number = subrule.split("<")
                prev = ranges[item]
                if prev[1] >= int(number):
                    ranges[item] = (prev[0], int(number) - 1)
        results.append(ranges)

    counts = []
    for ranges in results:
        count = 1
        count *= ranges["x"][1] - ranges["x"][0] + 1
        count *= ranges["m"][1] - ranges["m"][0] + 1
        count *= ranges["a"][1] - ranges["a"][0] + 1
        count *= ranges["s"][1] - ranges["s"][0] + 1
        counts.append(count)

    return sum(counts)


input = read_input()
write_output(solve_1(input), solve_2(input))
