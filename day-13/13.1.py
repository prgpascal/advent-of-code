import os
from typing import Sequence


def read_input():
    file_path = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(file_path) as f:
        n = int(f.readline().strip())
        bus_ids = [int(item.strip()) for item in f.readline().split(",") if item != "x"]
    return (n, bus_ids)


def solve(timestamp: int, bus_ids: Sequence):
    bus_with_arrivals = []
    for bus in bus_ids:
        bus_arrival = (timestamp - (timestamp % bus) + bus, bus)
        bus_with_arrivals.append(bus_arrival)

    first_bus = min(bus_with_arrivals)
    return (first_bus[0] - timestamp) * first_bus[1]


input = read_input()
print(solve(timestamp=input[0], bus_ids=input[1]))
