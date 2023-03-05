import os
from dataclasses import dataclass
from typing import Dict, List
from utils.io import write_output


@dataclass
class Node:
    name: str
    is_file: bool
    size: int
    parent: "Node"
    children: Dict[str, "Node"]


def create_dir_node(name, parent):
    return Node(name=name, is_file=False, size=0, parent=parent, children={})


def create_file_node(name, parent, size):
    return Node(
        name=name, is_file=True, size=int(size), parent=parent, children={}
    )


def read_input():
    root = current_dir = create_dir_node("/", None)
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            match line.strip().split(" "):
                case ["$", "cd", "/"]:
                    current_dir = root
                case ["$", "cd", ".."]:
                    current_dir = current_dir.parent
                case ["$", "cd", dir_name]:
                    current_dir = current_dir.children[dir_name]
                case ["$", "ls"]:
                    pass
                case ["dir", dir_name]:
                    dir_node = create_dir_node(dir_name, current_dir)
                    current_dir.children[dir_name] = dir_node
                case [file_size, file_name]:
                    file_node = create_file_node(file_name, current_dir, file_size)
                    current_dir.children[file_name] = file_node
    return root


def update_dirs_sizes(node: Node):
    if node.children:
        node.size = sum(map(update_dirs_sizes, node.children.values()))
    return node.size


def get_all_dirs(node: Node, target: List[Node]):
    if not node.is_file:
        target.append(node)
        for child_node in node.children.values():
            get_all_dirs(child_node, target)


def solve_1(input):
    dirs = []
    get_all_dirs(input, dirs)
    return sum([dir.size for dir in dirs if dir.size < 100000])


def solve_2(input):
    dirs = []
    get_all_dirs(input, dirs)
    current_free_space = 70000000 - input.size
    required_space = 30000000 - current_free_space
    return sorted([dir.size for dir in dirs if dir.size > required_space])[0]


input = read_input()
update_dirs_sizes(input)
write_output(solve_1(input), solve_2(input))
