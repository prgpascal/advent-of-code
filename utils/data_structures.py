from collections import namedtuple


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


_point_fields = ("x", "y", "z")
Point = namedtuple("Point", _point_fields, defaults=(None,) * len(_point_fields))
