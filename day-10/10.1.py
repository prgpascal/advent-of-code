import os


def read_input():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, "input.txt")
    lines = []
    with open(file_path) as f:
        lines = [int(l.strip()) for l in f.readlines()]
    return lines


def solve(lines):
    lines.insert(0, 0)
    lines.sort()
    lines.append(lines[-1] + 3)
    diff_dict = {}
    for i in range(0, len(lines) - 1):
        diff = lines[i+1] - lines[i]
        diff_dict[diff] = diff_dict.get(diff, 0) + 1
    return diff_dict


lines = read_input()
diff_dict = solve(lines)
print(diff_dict[1] * diff_dict[3])
