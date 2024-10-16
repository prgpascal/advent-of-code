import os
import re
from dataclasses import dataclass
from utils.io import write_output
from utils.utils import calculate_lcm


@dataclass
class Node:
    id: str
    left_node: str
    right_node: str


def read_input() -> tuple[str, dict[str, Node]]:
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        nodes = dict()
        instructions = file.readline().strip()
        file.readline()  # empty separator line
        for line in file:
            if match := re.search(r"(.*) = \((.*), (.*)\)", line.strip()):
                node_id, left_node, right_node = match.groups()
                nodes[node_id] = Node(node_id, left_node, right_node)
        return (instructions, nodes)


def count_steps(instructions: str, current_node: Node, nodes: dict[str, Node]):
    step_count = 0
    while not current_node.id.endswith("Z"):
        instruction = instructions[step_count % len(instructions)]
        current_node = (
            nodes[current_node.right_node]
            if instruction == "R"
            else nodes[current_node.left_node]
        )
        step_count += 1
    return step_count


def solve_1(input: tuple[str, dict[str, Node]]):
    instructions, nodes = input
    current_node = nodes["AAA"]
    return count_steps(instructions, current_node, nodes)


def solve_2(input: tuple[str, dict[str, Node]]):
    instructions, nodes = input
    all_starting_nodes = [n for n in nodes.keys() if n.endswith("A")]
    steps = []
    for node_id in all_starting_nodes:
        steps.append(count_steps(instructions, nodes[node_id], nodes))
    return calculate_lcm(steps)


input = read_input()
write_output(solve_1(input), solve_2(input))
