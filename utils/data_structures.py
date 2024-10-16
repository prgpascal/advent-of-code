from dataclasses import dataclass
from typing import Optional


class TreeNode:
    def __init__(
        self,
        value,
        left_node=None,
        right_node=None,
        parent_node=None,
        is_leaf=False,
    ):
        self.value = value
        self.left_node = left_node
        self.right_node = right_node
        self.parent_node = parent_node
        self.is_leaf = is_leaf

    def __str__(self):
        if self.is_leaf:
            return str(self.value)
        else:
            return f"[{self.left_node},{self.right_node}]"


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: Optional[int] = None

    def __lt__(self, other):
        if self.z is None and other.z is None:
            return self.x < other.x or self.y < other.y
        return self.x < other.x or self.y < other.y or self.z < other.z

    def __str__(self):
        if self.z is None:
            return f"({self.x}, {self.y})"
        return f"({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        if self.z is None:
            return iter((self.x, self.y))
        return iter((self.x, self.y, self.z))
