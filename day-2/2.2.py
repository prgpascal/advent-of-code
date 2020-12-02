import os


def read_file_lines(filename):
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, filename)
    lines = []
    with open(file_path) as f:
        while True:
            line = f.readline()
            if not line:
                break

            line_tuple = tuple(x for x in line.split())
            lines.append(line_tuple)

    return lines


def solve():
    lines = read_file_lines('input.txt')
    counter = 0
    for line in lines:
        pos1, pos2 = (int(x)-1 for x in line[0].split("-"))
        char = line[1][0]
        sequence = line[2]

        if (sequence[pos1] == char and sequence[pos2] != char) or \
           (sequence[pos2] == char and sequence[pos1] != char):
            counter += 1

    return counter


print(solve())
