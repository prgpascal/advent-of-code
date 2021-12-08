import os
from collections import defaultdict


UNIQUE_SEGMENTS_LENGTH = {
    3: 7,
    4: 4,
    2: 1,
    7: 8,
}


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            signal_patterns, output_values = line.strip().split(" | ")
            input.append((signal_patterns.split(), output_values.split()))
    return input


def solve_1(input):
    counter = 0
    for line in input:
        output_value = line[1]
        for value in output_value:
            if len(value) in UNIQUE_SEGMENTS_LENGTH:
                counter += 1
    return counter


def find_segments_configuration(signal_patterns):
    found = defaultdict(set)
    to_remove = []

    # segments with unique lenghts
    for signal in signal_patterns:
        k = UNIQUE_SEGMENTS_LENGTH.get(len(signal))
        if k is not None:
            found[k] = set(signal)
            to_remove.append(signal)
    for s in to_remove:
        signal_patterns.remove(s)

    # find 9
    for s in signal_patterns:
        if len(s) == 6 and len((set(s).union(found[4]))) == 6:
            found[9] = set(s)
            to_remove = s
            break
    signal_patterns.remove(to_remove)

    # find 6
    for s in signal_patterns:
        if len(s) == 6 and len((set(s).union(found[1]))) == 7:
            found[6] = set(s)
            to_remove = s
            break
    signal_patterns.remove(to_remove)

    # find 0
    for s in signal_patterns:
        if len(s) == 6:
            found[0] = set(s)
            to_remove = s
            break
    signal_patterns.remove(to_remove)

    # find 3
    for s in signal_patterns:
        if len(set(s).difference(found[1])) == 3:
            found[3] = set(s)
            to_remove = s
            break
    signal_patterns.remove(to_remove)

    # find 5
    for s in signal_patterns:
        if len(set(s).difference(found[4])) == 2:
            found[5] = set(s)
            to_remove = s
            break
    signal_patterns.remove(to_remove)

    # last one is 2
    found[2] = set(signal_patterns[0])

    return found


def solve_2(input):
    all_results = []

    for line in input:
        signal_patterns, output_values = line
        config = find_segments_configuration(signal_patterns)
        response = []
        for out in output_values:
            response += [str(k) for k, v in config.items() if set(v) == set(out)]
        all_results.append(int("".join(response)))

    return sum(all_results)


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


input = read_input()
write_output(solve_1(input), solve_2(input))
