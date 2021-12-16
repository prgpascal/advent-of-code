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

    for _ in range(10):
        expanded = []
        for i in range(len(polymer_template)):
            expanded.append(polymer_template[i])
            if i < len(polymer_template) - 1:
                pair = "".join(polymer_template[i : i + 2])
                expanded.append(rules[pair])
        polymer_template = expanded

    ordered = Counter(polymer_template).most_common()
    return ordered[0][1] - ordered[-1][1]


def solve_2():
    polymer_template, rules = read_input()
    pairs_frequency = {k: 0 for k in rules.keys()}
    char_counter = Counter(polymer_template)

    for i in range(len(polymer_template) - 1):
        pair = "".join(polymer_template[i : i + 2])
        pairs_frequency[pair] += 1

    for i in range(40):
        for pair, frequence in pairs_frequency.copy().items():
            if frequence > 0:
                new_char = rules[pair]
                pairs_frequency[f"{pair[0]}{new_char}"] += frequence
                pairs_frequency[f"{new_char}{pair[1]}"] += frequence
                pairs_frequency[pair] -= frequence
                char_counter[new_char] += frequence

    ordered = char_counter.most_common()
    return ordered[0][1] - ordered[-1][1]


write_output(solve_1(), solve_2())
