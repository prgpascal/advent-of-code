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


def is_valid_ticket(ticket, fields_set):
    return all(int(number) in fields_set for number in ticket.split(","))


def solve(input):
    all_fields = {}
    all_field_names = set()
    all_fields_union = set()
    for field in input["fields"]:
        for match in re.finditer(FIELDS_REGEX, field):
            field_name = match.group(1)
            all_field_names.add(field_name)
            all_fields.setdefault(field_name, set()).update(
                range(int(match.group(2)), int(match.group(3)) + 1)
            )
            all_fields.setdefault(field_name, set()).update(
                range(int(match.group(4)), int(match.group(5)) + 1)
            )
            all_fields_union.update(all_fields[field_name])

    valid_nearby_tickets = [
        nearby
        for nearby in input["nearby"]
        if is_valid_ticket(nearby, all_fields_union)
    ]

    your_ticket = input["your"][0].split(",")
    n = len(your_ticket)
    assigned_fields = {}
    for i in range(0, n):
        assigned_fields[i] = set(all_field_names)

    for nearby in valid_nearby_tickets:
        for i, near in enumerate(nearby.split(",")):
            if len(assigned_fields[i]) > 1:
                fields_to_remove = [
                    key
                    for key in assigned_fields[i]
                    if int(near) not in all_fields[key]
                ]

                for f in fields_to_remove:
                    assigned_fields[i].remove(f)

                if len(assigned_fields[i]) == 1:
                    for k in assigned_fields:
                        if k != i:
                            assigned_fields[k].discard(list(assigned_fields[i])[0])

    sorted_assigned_fields = [(len(v), (k, v)) for k, v in assigned_fields.items()]
    sorted_assigned_fields.sort()
    sorted_assigned_fields = {b[0]: b[1] for _, b in sorted_assigned_fields}

    already_seen = set()
    result = 1
    for k, v in sorted_assigned_fields.items():
        field_name = list(v - already_seen)[0]
        if field_name.startswith("departure"):
            result *= int(your_ticket[k])
        already_seen = already_seen | v

    return result


input = read_input()
print(solve(input))
