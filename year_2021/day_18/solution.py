import os
from utils.io import write_output
from utils.data_structures import TreeNode
import math
from itertools import product


def read_input():
    input = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = [line.strip() for line in file.readlines()]
    return input


def build_tree(line, parent_node=None):
    if line.isdecimal():
        return TreeNode(int(line), is_leaf=True, parent_node=parent_node)

    line = line[1:-1]
    n_brackets = 0
    for index, char in enumerate(line):
        n_brackets += 1 if char == "[" else 0
        n_brackets -= 1 if char == "]" else 0

        if n_brackets == 0 and char == ",":
            # found the middle index, can build the node
            node = TreeNode(None, parent_node=parent_node)
            left_node = build_tree(line[:index], parent_node=node)
            right_node = build_tree(line[index + 1 :], parent_node=node)
            node.right_node = right_node
            node.left_node = left_node
            return node


def add(left_node, right_node):
    new_node = TreeNode(None, left_node=left_node, right_node=right_node)
    left_node.parent_node = new_node
    right_node.parent_node = new_node
    return new_node


def propagate_right(node, number):
    if not node.parent_node:
        # root node reached
        return

    if node.parent_node.right_node != node:
        node = node.parent_node.right_node
        while node:
            if node.is_leaf:
                node.value += number
                break
            else:
                if node.left_node:
                    node = node.left_node
                else:
                    node = node.right_node
    else:
        propagate_right(node.parent_node, number)


def propagate_left(node, number):
    if not node.parent_node:
        # root node reached
        return

    if node.parent_node.left_node != node:
        node = node.parent_node.left_node
        while node:
            if node.is_leaf:
                node.value += number
                break
            else:
                if node.right_node:
                    node = node.right_node
                else:
                    node = node.left_node
    else:
        propagate_left(node.parent_node, number)


def explode(node, layer):
    if node:
        if layer < 4:
            node.left_node = explode(node.left_node, layer + 1)
            node.right_node = explode(node.right_node, layer + 1)
        elif not node.is_leaf:
            # this layer should be exploded
            propagate_right(node, node.right_node.value)
            propagate_left(node, node.left_node.value)
            node = TreeNode(0, is_leaf=True, parent_node=node.parent_node)
    return node


def split(node):
    splitted = False
    if node:
        if node.is_leaf:
            if node.value >= 10:
                new_node = TreeNode(None, parent_node=node.parent_node)
                new_node.right_node = build_tree(
                    str(math.ceil(int(node.value) / 2)), parent_node=new_node
                )
                new_node.left_node = build_tree(
                    str(math.floor(int(node.value) / 2)), parent_node=new_node
                )
                return (new_node, True)
        else:
            splitted_left = splitted_right = False
            left_node, splitted_left = split(node.left_node)
            node.left_node = left_node
            if not splitted_left:
                right_node, splitted_right = split(node.right_node)
                node.right_node = right_node
            splitted = splitted_left or splitted_right
    return (node, splitted)


def calculate_result(node):
    if node.is_leaf:
        return node.value
    return 3 * calculate_result(node.left_node) + 2 * calculate_result(node.right_node)


def apply_reduce(node):
    should_reduce = True
    while should_reduce:
        node = explode(node, 0)
        node, should_reduce = split(node)
    return node


def solve_1():
    input = read_input()
    root = build_tree(input[0])
    for node in input[1:]:
        node = build_tree(node)
        root = add(root, node)
        root = apply_reduce(root)
    return calculate_result(root)


def solve_2():
    input = read_input()
    pairs = [(x, y) for (x, y) in product(input, repeat=2) if x != y]
    results = []
    for node_1, node_2 in pairs:
        root = add(build_tree(node_1), build_tree(node_2))
        root = apply_reduce(root)
        results.append(calculate_result(root))
    return max(results)


write_output(solve_1(), solve_2())
