from abc import ABC, abstractmethod
from typing import Iterable
from collections import deque


# --- Abstract Node Interface ---
class Node(ABC):
    @abstractmethod
    def get_children(self) -> Iterable['Node']:
        """Return an iterable of child nodes"""
        pass


class Tree:
    def __init__(self, root: Node | list[Node]):
        if isinstance(root, Node):
            self.roots = [root]
        elif isinstance(root, list) and all(isinstance(n, Node) for n in root):
            self.roots = root
        else:
            raise TypeError("root must be a Node or a list of Node objects")
        self._current = None
        self._fallback = None

    def set_current(self, node):
        self._current = node

    def breadth_first(self):
        """
        Yield nodes in breadth-first order up to the level of self._current.

        Nodes are yielded level by level from the tree's root(s). Traversal
        stops after yielding all nodes at the same level as self._current;
        children of those nodes are not visited.
        """
        level_reached = False
        current_level = deque(self.roots)
        next_level_nodes = []

        while current_level or next_level_nodes:
            if not current_level:
                current_level = deque(next_level_nodes)
                next_level_nodes = []

            node = current_level.popleft()
            yield node

            if self._current == node:
                level_reached = True
                next_level_nodes.clear()

            if not level_reached:
                next_level_nodes.extend(node.children)

    def current_children(self):
        for child in self._current.children:
            yield child
