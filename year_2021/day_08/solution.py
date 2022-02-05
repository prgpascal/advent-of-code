import os
from collections import defaultdict
from utils.io import write_output

# { length: signal }
UNIQUE_SIGNAL_LENGTHS = {
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


def solve_1():
    input = read_input()
    counter = 0
    for line in input:
        output_value = line[1]
        for value in output_value:
            if len(value) in UNIQUE_SIGNAL_LENGTHS:
                counter += 1
    return counter


def find_configuration(signal_patterns):
    found = defaultdict(set)

    # pre-load signals with unique lenghts
    for signal in signal_patterns:
        signal_length = len(signal)
        signal_set = set(signal)
        if signal_length in UNIQUE_SIGNAL_LENGTHS:
            found[UNIQUE_SIGNAL_LENGTHS[signal_length]] = signal_set

    for signal in signal_patterns:
        signal_length = len(signal)
        signal_set = set(signal)
        if signal_length == 6 and len(signal_set.union(found[4])) == 6:
            found[9] = signal_set
        elif signal_length == 6 and len(signal_set.union(found[1])) == 7:
            found[6] = signal_set
        elif signal_length == 6:
            found[0] = signal_set
        elif signal_length == 5 and len(signal_set.difference(found[1])) == 3:
            found[3] = signal_set
        elif signal_length == 5 and len(signal_set.difference(found[4])) == 2:
            found[5] = signal_set
        elif signal_length == 5:
            found[2] = signal_set

    return found


def solve_2():
    input = read_input()
    all_results = []

    for line in input:
        signal_patterns, output_values = line
        config = find_configuration(signal_patterns)
        response = []
        for out in output_values:
            response += [str(k) for k, v in config.items() if set(v) == set(out)]
        all_results.append(int("".join(response)))

    return sum(all_results)


write_output(solve_1(), solve_2())
