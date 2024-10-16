import os
import inspect
from print_tree import print_tree


class print_binary_tree(print_tree):
    def get_children(self, node):
        l_child = node.left_node
        r_child = node.right_node
        if r_child is None and l_child is None:
            return []
        else:
            l_child = l_child or "None"
            r_child = r_child or "None"
            return [r_child, l_child]

    def get_node_str(self, node):
        return str(node)


def write_output(output_1, output_2):
    filename = inspect.stack()[1].filename
    dirname = os.path.dirname(filename)

    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(dirname, "output.txt"), "w") as file:
        file.write(output)


def print_matrix(matrix, as_string=False):
    for row in matrix:
        x = row if not as_string else "".join([str(x) for x in row])
        print(x)
    print()


def create_matrix(rows, columns, char=" "):
    return [[char for _ in range(columns)] for _ in range(rows)]


def get_matrix_column(matrix, j):
    return "".join([row[j] for row in matrix])