import os


def solve():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [l.strip() for l in f.readlines()]

    row_len = len(lines[0])
    counter = 0
    for i, line in enumerate(lines[1:], start=1):
        pos = (3 * i) % row_len
        if line[pos] == "#":
            counter += 1

    return counter


print(solve())
