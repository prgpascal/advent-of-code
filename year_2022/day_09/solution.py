import os
from utils.io import write_output


def is_not_touching(a, b):
    min_x = min(a[0], b[0])
    max_x = max(a[0], b[0])
    min_y = min(a[1], b[1])
    max_y = max(a[1], b[1])
    return not (max_x - min_x <= 1 and max_y - min_y <= 1)


class State:
    def __init__(self, knots):
        self.visited: set[tuple[int, int]] = set()
        self.visited.add((0, 0))
        self.knots = knots

    def move(self, knot_index: int, direction: str, should_count: bool):
        knot = self.knots[knot_index]
        # move the desired knot
        match direction:
            case "R":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] + 1,
                    self.knots[knot_index][1],
                )
            case "L":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] - 1,
                    self.knots[knot_index][1],
                )
            case "U":
                self.knots[knot_index] = (
                    self.knots[knot_index][0],
                    self.knots[knot_index][1] + 1,
                )
            case "D":
                self.knots[knot_index] = (
                    self.knots[knot_index][0],
                    self.knots[knot_index][1] - 1,
                )
            case "RU" | "UR":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] + 1,
                    self.knots[knot_index][1] + 1,
                )
            case "RD" | "DR":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] + 1,
                    self.knots[knot_index][1] - 1,
                )
            case "LU" | "UL":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] - 1,
                    self.knots[knot_index][1] + 1,
                )
            case "LD" | "DL":
                self.knots[knot_index] = (
                    self.knots[knot_index][0] - 1,
                    self.knots[knot_index][1] - 1,
                )

        knot = self.knots[knot_index]

        # move next knot
        if knot_index < len(self.knots) - 1:
            new_knot = self.knots[knot_index + 1]
            if is_not_touching(self.knots[knot_index], new_knot):
                direction = ""
                if knot[0] > new_knot[0]:
                    direction += "R"
                if knot[0] < new_knot[0]:
                    direction += "L"
                if knot[1] < new_knot[1]:
                    direction += "D"
                if knot[1] > new_knot[1]:
                    direction += "U"
                self.move(knot_index + 1, direction, True)

        if should_count:
            self.visited.add(self.knots[-1])


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        return [line.strip().split(" ") for line in file.readlines()]


def solve_1(input):
    state = State([(0, 0), (0, 0)])
    for direction, steps in input:
        for _ in range(int(steps)):
            state.move(0, direction, True)
    return len(state.visited)


def solve_2(input):
    state = State(
        [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    )
    for direction, steps in input:
        for _ in range(int(steps)):
            state.move(0, direction, True)
    return len(state.visited)


input = read_input()
write_output(solve_1(input), solve_2(input))
