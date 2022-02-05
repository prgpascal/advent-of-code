import itertools
import os
from collections import Counter

import numpy as np
from utils.io import write_output


# Solved with the help of the Reddit community. This exercise was so challenging (>_<)"
# Credit:
# - https://github.com/MartinSeeler/Advent-of-Code/blob/master/2021/day19/solution.py


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        scanners = []
        current_scanner = []
        for line in file.readlines():
            line = line.strip()
            if line.startswith("---"):
                continue
            if line != "":
                current_scanner.append([int(x) for x in line.split(",")])
            elif len(current_scanner) > 0:
                scanners.append(np.array(current_scanner))
                current_scanner = []
        scanners.append(np.array(current_scanner))
        return scanners


def all_orientations(scanner):
    for dir_x, dir_y in itertools.permutations(range(3), 2):
        for sign_x, sign_y in itertools.product((-1, 1), (-1, 1)):
            x_vec = np.zeros((3,))
            y_vec = np.zeros((3,))
            x_vec[dir_x] = sign_x
            y_vec[dir_y] = sign_y
            z_vec = np.cross(x_vec, y_vec)
            yield np.array(
                [
                    np.array(
                        [
                            np.dot(x_vec, beacon),
                            np.dot(y_vec, beacon),
                            np.dot(z_vec, beacon),
                        ]
                    )
                    for beacon in scanner
                ]
            ).reshape(-1, 3)


def solve(scanners):
    beacons = scanners[0]
    remaining = scanners[1:]
    scanners = set([tuple([0, 0, 0])])
    while len(remaining) > 0:
        for i, scanner in enumerate(remaining):
            for o in all_orientations(scanner):
                c = Counter()
                for p2 in o:
                    for p1 in beacons:
                        c[tuple(p1 - p2)] += 1
                msc = c.most_common()[0]
                if msc[1] >= 12:
                    v = np.array(msc[0])
                    target = o + v
                    scanners.add(tuple(v))
                    beacons = np.concatenate((beacons, target))
                    remaining.pop(i)
                    break
    return scanners, beacons


def solve_1():
    input = read_input()
    beacons = solve(input)[1]
    return len(set([tuple(i) for i in beacons.tolist()]))


def solve_2():
    input = read_input()
    scanners = solve(input)[0]
    return int(
        np.max(
            [
                np.sum(np.abs(np.array(i) - np.array(j)))
                for i in scanners
                for j in scanners
                if i != j
            ]
        )
    )


write_output(solve_1(), solve_2())
