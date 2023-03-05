import os
import re
from dataclasses import dataclass
from typing import Dict
from utils.data_structures import TreeNode
from utils.io import write_output

NUMBER_INPUT = r"(.*): (\d+)"
OPERATION_INPUT = r"(.*): (.*) (.) (.*)"


@dataclass
class Monkey:
    name: str
    first_operand: str | None
    second_operand: str | None
    operator: str | None
    number: float | None


def read_input() -> Dict[str, Monkey]:
    monkeys = dict()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            if match := re.search(OPERATION_INPUT, line.strip()):
                name = match.group(1)
                monkeys[name] = Monkey(
                    name=name,
                    first_operand=match.group(2),
                    second_operand=match.group(4),
                    operator=match.group(3),
                    number=None,
                )
            elif match := re.search(NUMBER_INPUT, line.strip()):
                name = match.group(1)
                monkeys[name] = Monkey(
                    name=name,
                    first_operand=None,
                    second_operand=None,
                    operator=None,
                    number=float(match.group(2)),
                )
    return monkeys


def create_tree_node(monkeys: Dict[str, Monkey], name: str) -> TreeNode:
    current_monkey = monkeys[name]
    node = TreeNode(current_monkey)
    if current_monkey.first_operand is not None:
        left_node = create_tree_node(monkeys, current_monkey.first_operand)
        left_node.parent_node = node
        node.left_node = left_node
    if current_monkey.second_operand is not None:
        right_node = create_tree_node(monkeys, current_monkey.second_operand)
        right_node.parent_node = node
        node.right_node = right_node
    return node


def update_nodes_numbers(node: TreeNode):
    if node.value.number is None:
        if node.left_node is not None and node.right_node is not None:
            update_nodes_numbers(node.left_node)
            update_nodes_numbers(node.right_node)

            if (
                node.left_node.value.number is not None
                and node.right_node.value.number is not None
            ):
                node.value.number = do_operation(
                    node.value.operator,
                    node.left_node.value.number,
                    node.right_node.value.number,
                )


def do_operation(operator, a, b, result=None, inverse=False) -> float:
    if not inverse:
        match operator:
            case "+":
                return a + b
            case "-":
                return a - b
            case "*":
                return a * b
            case "/":
                return a / b
    else:
        match operator:
            case "+":
                if a is None:
                    return result - b
                elif b is None:
                    return result - a
            case "-":
                if a is None:
                    return result + b
                if b is None:
                    return a - result
            case "*":
                if a is None:
                    return result / b
                if b is None:
                    return result / a
            case "/":
                if a is None:
                    return b * result
                elif b is None:
                    return a / result

    raise Exception("Cannot perform operation")


def compute_human_number(node: TreeNode, expected_result: float) -> float:
    if node.right_node is not None and node.left_node is not None:
        right_number = node.right_node.value.number
        left_number = node.left_node.value.number
        inverse_operation_result = do_operation(
            node.value.operator, left_number, right_number, expected_result, True
        )
        if node.left_node.value.name == "humn" or node.right_node.value.name == "humn":
            return inverse_operation_result

        if right_number is not None:
            return compute_human_number(node.left_node, inverse_operation_result)
        elif left_number is not None:
            return compute_human_number(node.right_node, inverse_operation_result)

    raise Exception("Cannot compute the 'humn' number")


def solve_1():
    input = read_input()
    root_node = create_tree_node(input, "root")
    update_nodes_numbers(root_node)
    return int(root_node.value.number)


def solve_2():
    input = read_input()
    input["humn"].number = None
    root_node = create_tree_node(input, "root")
    update_nodes_numbers(root_node)

    if root_node.right_node is not None and root_node.left_node is not None:
        right_number = root_node.right_node.value.number
        left_number = root_node.left_node.value.number
        if right_number is not None:
            return int(compute_human_number(root_node.left_node, right_number))
        elif left_number is not None:
            return int(compute_human_number(root_node.right_node, left_number))

    raise Exception("Cannot navigate the tree")


write_output(solve_1(), solve_2())
