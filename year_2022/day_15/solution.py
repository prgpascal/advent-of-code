import os
import re
from collections import namedtuple
from utils.io import write_output
from utils.data_structures import Point
from utils.utils import calculate_manhattan_distance

INPUT_REGEX = r"x=(-*\d+).*y=(-*\d+).*x=(-*\d+).*y=(-*\d+)"

Pair = namedtuple("Pairs", ["sensor", "beacon"])


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            if match := re.search(INPUT_REGEX, line):
                sensor = Point(int(match.group(1)), int(match.group(2)))
                beacon = Point(int(match.group(3)), int(match.group(4)))
                input.append(Pair(sensor, beacon))
    return input


def get_points_in_axis(points, min, max):
    to_remove = set()
    for point in points:
        if point.x in range(min, max + 1):
            to_remove.add(point)
    return to_remove


def calculate_max_range(segments, points_in_target_axis):
    count = 0
    to_remove = set()
    min = segments[0][0]
    max = segments[0][1]

    for a, b in segments[1:]:
        if a in range(min, max + 1) and b in range(min, max + 1):
            continue
        elif a <= max and b >= max:
            max = b
        else:
            to_remove.update(get_points_in_axis(points_in_target_axis, min, max))
            count += max - min
            min = a
            max = b

    to_remove.update(get_points_in_axis(points_in_target_axis, min, max))
    count += max - min
    count += len(points_in_target_axis.difference(to_remove))

    return count


def get_segments_for_row(input, target_y, is_bounded, bound_limit=0):
    segments = []
    for (sensor, beacon) in input:
        distance = calculate_manhattan_distance(sensor, beacon)
        if (sensor.y <= target_y and sensor.y + distance >= target_y) or (
            sensor.y >= target_y and sensor.y - distance <= target_y
        ):
            height = calculate_manhattan_distance(sensor, Point(sensor.x, target_y))
            horizontal_axis = abs(distance - height)
            segment = (sensor.x - horizontal_axis, sensor.x + horizontal_axis)
            if is_bounded:
                if (segment[0] < 0) and (segment[1] < 0):
                    continue
                new_min = segment[0] if segment[0] >= 0 else 0
                new_max = segment[1] if segment[1] <= bound_limit else bound_limit
                segment = (new_min, new_max)
            segments.append(segment)

    segments = sorted(segments)
    return segments


def solve_1(input):
    target_y = 2000000
    all_beacons = set([x for s, x in input])
    all_sensors = set([s for s, x, in input])
    union = all_beacons.union(all_sensors)
    points_in_target_axis = set([p for p in union if p.y == target_y])
    segments = get_segments_for_row(input, target_y, False)
    result = calculate_max_range(segments, points_in_target_axis)
    return result


def solve_2(input):
    # Idea: break calculate_max_range (line #44) when:
    # a == 3293022
    # Solution: 13172087230812 = 3293021 * 4000000 + 3230812

    # for i in range(4000000, -1, -1):
    #     all_beacons = set([x for s, x in input])
    #     all_sensors = set([s for s, x, in input])
    #     union = all_beacons.union(all_sensors)
    #     points_in_target_axis = set([p for p in union if p.y == i])
    #     segments = get_segments_for_row(input, i, True, 4000000)
    #     result = calculate_max_range(segments, points_in_target_axis)
    return "??"


input = read_input()
write_output(solve_1(input), solve_2(input))
