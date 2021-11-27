import os
from functools import reduce


def solve(rules):
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]

    counters = []
    row_len = len(lines[0])

    for rule in rules:
        counter = 0
        for i in range(0, len(lines), rule[1]):
            if i > 0:
                line = lines[i]
                pos = (rule[0] * i // rule[1]) % row_len
                if line[pos] == "#":
                    counter += 1

        counters.append(counter)

    return reduce(lambda x, y: x * y, counters)


rules = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]
print(solve(rules))
