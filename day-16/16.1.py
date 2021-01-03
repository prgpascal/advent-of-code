import os
import re

FIELDS_REGEX = r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)"


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        is_reading = "fields"
        input = {}
        for line in file:
            line = line.strip()
            if line == "":
                pass
            elif line == "your ticket:":
                is_reading = "your"
            elif line == "nearby tickets:":
                is_reading = "nearby"
            else:
                input.setdefault(is_reading, []).append(line)
    return input


def solve(input):
    fields_set = set()
    for field in input["fields"]:
        for match in re.finditer(FIELDS_REGEX, field):
            fields_set.update(range(int(match.group(2)), int(match.group(3)) + 1))
            fields_set.update(range(int(match.group(4)), int(match.group(5)) + 1))

    invalid_seats = list()
    for nearby in input["nearby"]:
        for seat in (int(n) for n in nearby.split(",")):
            if seat not in fields_set:
                invalid_seats.append(seat)

    return sum(invalid_seats)


input = read_input()
print(solve(input))
