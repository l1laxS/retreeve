class TreeNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

    def add_child(self, child: "TreeNode"):
        child.parent = self
        self.children.append(child)


class ParseTree:
    """
    A tree of parsed objects, representing the output of a hierarchical parser.

    This tree mirrors the structure of the parsed input file. Each node wraps
    a parsed object (e.g., a block, section, etc.). The tree tracks a current
    node, which is the active context for parsing new lines.
    """

    def __init__(self, root_objects: list):
        self._root_nodes = [TreeNode(obj) for obj in root_objects]
        self._current = self._root_nodes[-1] if self._root_nodes else None

    def get_current(self):
        """Return the current parsed object."""
        return self._current.value if self._current else None

    def move_current_up(self) -> bool:
        """
        Move the current pointer to its parent.

        Returns:
            True if moved to parent successfully,
            False if already at root.
        """
        if self._current is None or self._current.parent is None:
            return False
        self._current = self._current.parent
        return True

    def add_child(self, obj):
        """
        Add a new parsed object as a child of the current node.

        The new node becomes the current node.
        """
        new_node = TreeNode(obj)

        if self._current is None:
            # No current node: treat as top-level root
            self._root_nodes.append(new_node)
        else:
            self._current.add_child(new_node)

        self._current = new_node

    def add_sibling(self, obj):
        """
        Add a new parsed object as a sibling of the current node.

        The new node becomes the current node.
        """
        new_node = TreeNode(obj)

        if self._current is None or self._current.parent is None:
            # Current is at root level
            self._root_nodes.append(new_node)
        else:
            self._current.parent.add_child(new_node)

        self._current = new_node

    def insert_beside_current(self, obj):
        """
        Add a fallback parsed object beside the current node.

        Unlike add_sibling(), this does not change the current node.
        """
        new_node = TreeNode(obj)

        if self._current is None or self._current.parent is None:
            self._root_nodes.append(new_node)
        else:
            self._current.parent.add_child(new_node)

    def __iter__(self):
        """Iterate over all parsed objects in the tree (pre-order)."""
        def walk(node):
            yield node.value
            for child in node.children:
                yield from walk(child)

        for root in self._root_nodes:
            yield from walk(root)

    def debug_print(self):
        """Print the tree structure for debugging."""

        def walk(node, depth):
            prefix = "  " * depth
            print(f"{prefix}- {type(node.value).__name__}")
            for child in node.children:
                walk(child, depth + 1)

        for root in self._root_nodes:
            walk(root, 0)

