import os


def read_groups():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    groups = []
    with open(file_path) as f:
        tmp_group = set()
        for line in (line.strip() for line in f):
            if line == "":
                groups.append(tmp_group)
                tmp_group = set()
            else:
                tmp_group.update(line)
        groups.append(tmp_group)

    return groups


def solve(groups):
    return sum([len(group) for group in groups])


print(solve(read_groups()))
