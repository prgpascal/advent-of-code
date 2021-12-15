import os
import inspect


def write_output(output_1, output_2):
    filename = inspect.stack()[1].filename
    dirname = os.path.dirname(filename)

    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(dirname, "output.txt"), "w") as file:
        file.write(output)


def print_matrix(matrix, as_string=False):
    for row in matrix:
        x = row if not as_string else ''.join([str(x) for x in row])
        print(x)
    print()


def create_matrix(rows, columns, char=" "):
    return [[char for _ in range(columns)] for _ in range(rows)]
