import os
from collections import Counter
from utils.io import write_output


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        polymer_template = list(file.readline().strip())
        file.readline()
        rules = dict()
        for line in file:
            a, b = line.strip().split(" -> ")
            rules[a] = b
        return (polymer_template, rules)


def solve_1():
    polymer_template, rules = read_input()
    resulting_list = polymer_template
    for _ in range(10):
        tmp_list = []
        for i in range(len(resulting_list)):
            tmp_list.append(resulting_list[i])
            if i < len(resulting_list) - 1:
                pair = "".join(resulting_list[i : i + 2])
                tmp_list.append(rules[pair])
        resulting_list = tmp_list
    order = Counter(resulting_list).most_common()
    return order[0][1] - order[-1][1]


def solve_2():
    return ""


write_output(solve_1(), solve_2())
