import os


def solve():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    for x, y in ((int(x), int(y)) for x in lines for y in lines):
        if x + y == 2020:
            return x*y


print(solve())
