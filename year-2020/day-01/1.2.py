import os


def solve():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    for x, y, z in ((int(x), int(y), int(z)) for x in lines for y in lines for z in lines):
        if x + y + z == 2020:
            return x*y*z


print(solve())
