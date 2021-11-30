import os

def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        # line by line
        for line in file:
            line = line.strip()

        # all lines
        input = [line.strip() for line in file.readlines()]

    return input


def solve(input):
    pass


def write_output(output):
    f = open("output.txt", "w")
    f.write(output)
    f.close()


input = read_input()
output = solve(input)
write_output(output)
