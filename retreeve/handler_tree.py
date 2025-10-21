from abc import ABC, abstractmethod
from typing import Iterable, Type
from collections import deque


# --- Abstract Node Interface ---
class Node(ABC):
    @abstractmethod
    def get_children(self) -> Iterable[Type['Node']]:
        """Return an iterable of child nodes"""
        pass


class HandlerTree:
    def __init__(self, root: Type[Node] | list[Type[Node]]):
        if isinstance(root, type) and issubclass(root, Node):
            self.roots = [root]
        elif isinstance(root, list) and \
            all(isinstance(cls, type) and issubclass(cls, Node)
                for cls in root):
            self.roots = root
        else:
            raise TypeError("root must be a Node type or a list of Node types")
        self._current = None
        self._fallback = None

    def set_current(self, node):
        self._current = node

    def move_current_up(self) -> bool:
        """
        Move the current pointer to its parent.

        Returns:
            True if the move succeeded (i.e., there was a parent),
            False if already at the root (no parent).
        """
        if self._current is None:
            return False

        parent = self._current.parent
        if parent is None:
            return False

        self._current = parent
        return True

    def breadth_first(self):
        """
        Yield nodes in breadth-first order up to the level of self._current.

        Nodes are yielded level by level from the tree's root(s). Traversal
        stops after yielding all nodes at the same level as self._current;
        children of those nodes are not visited.
        """
        level_reached = False
        current_level = deque((node, 0) for node in self.roots)
        next_level_nodes = []

        while current_level or next_level_nodes:
            if not current_level:
                current_level = deque(next_level_nodes)
                next_level_nodes = []

            node, depth = current_level.popleft()
            yield node, depth

            if self._current == node:
                level_reached = True
                next_level_nodes.clear()

            if not level_reached:
                for child in node.children:
                    next_level_nodes.append((child, depth + 1))

    def current_children(self):
        for child in self._current.children:
            yield child
