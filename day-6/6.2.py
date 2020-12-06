import os


def read_groups():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'input.txt')
    groups = []
    with open(file_path) as f:
        tmp_group = set()
        first_person = True
        for line in (line.strip() for line in f):
            if line == "":
                groups.append(tmp_group)
                tmp_group = set()
                first_person = True
            else:
                if first_person:
                    tmp_group.update(line)
                    first_person = False
                else:
                    tmp_group = tmp_group.intersection(line)

        groups.append(tmp_group)

    return groups


def solve(groups):
    return sum([len(group) for group in groups])


print(solve(read_groups()))
