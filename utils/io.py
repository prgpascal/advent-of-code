import os
import inspect


def write_output(output_1, output_2):
    filename = inspect.stack()[1].filename
    dirname = os.path.dirname(filename)

    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(dirname, "output.txt"), "w") as file:
        file.write(output)


def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()


def create_matrix(rows, columns, char=" "):
    return [[char for _ in range(columns)] for _ in range(rows)]
