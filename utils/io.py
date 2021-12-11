import os


def write_output(dirname, output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(dirname, "output.txt"), "w") as file:
        file.write(output)


def print_matrix(matrix):
    for row in matrix:
        print(row)
    print()
