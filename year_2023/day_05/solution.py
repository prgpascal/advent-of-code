import os
from dataclasses import dataclass
from utils.io import write_output


@dataclass
class MyMap:
    name: str
    ranges: list[tuple]

    def map_output(self, x):
        for destination_start, source_start, length in self.ranges:
            if x >= source_start and x <= source_start + length:
                delta = x - source_start
                return destination_start + delta
        return x


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        seeds = [int(x) for x in file.readline().strip().split(": ")[1].split(" ")]
        maps: list[MyMap] = []
        current_map = None
        for line in file:
            line = line.strip()
            if line == "":
                continue
            elif line[0].isalpha():
                if current_map is not None:
                    maps.append(current_map)
                current_map = MyMap(line.split(":")[0], [])
            elif current_map is not None:
                numbers = tuple(int(x) for x in line.split(" "))
                current_map.ranges.append(numbers)

        if current_map is not None:
            maps.append(current_map)

    return (seeds, maps)


def solve(seed, maps):
    for map in maps:
        seed = map.map_output(seed)
    return seed


def solve_1(input):
    seeds, maps = input
    return min(solve(seed, maps) for seed in seeds)


def solve_2(input):
    seeds, maps = input
    seeds = [seeds[i : i + 2] for i in range(0, len(seeds), 2)]

    # reverse the maps, and invert the source/destination ranges, so we can proceed from the last map to the first one
    reversed_maps = list(reversed(maps))
    for map in reversed_maps:
        map.ranges = [(r[1], r[0], r[2]) for r in map.ranges]

    # perform a coarse-grained search, by incrementing the seed by "step"
    COARSE_STEP = 10000
    seed_found = None
    seed = 0
    while seed_found is None:
        seed += COARSE_STEP
        sol = solve(seed, reversed_maps)
        if any(sol >= s[0] and sol <= s[0] + s[1] for s in seeds):
            seed_found = seed

    # perform a fine-grained search, to find the lowest valid seed
    for seed in range(seed_found - COARSE_STEP, seed_found):
        sol = solve(seed, reversed_maps)
        if any(sol >= s[0] and sol <= s[0] + s[1] for s in seeds):
            return seed


input = read_input()
write_output(solve_1(input), solve_2(input))
