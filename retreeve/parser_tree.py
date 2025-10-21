class ParseTree:
    """
    A tree of parsed objects, representing the output of a hierarchical parser.

    This tree mirrors the structure of the parsed input file. Each node wraps
    a parsed object (e.g., a block, section, etc.). The tree tracks a current
    node, which is the active context for parsing new lines.
    """

    def __init__(self):
        self._root_nodes = []
        self._current = None

    def get_current(self):
        """Return the current parsed object."""
        return self._current.value if self._current else None

    def set_current(self, obj):
        self._current = obj

    def current_and_ancestors(self):
        node = self._current
        while node:
            yield node
            node = node.parent

    def move_up_to(self, depth: int):
        """
        Move the current node up to the specified depth.

        Depth 0 refers to the root level, depth 1 to the root's child, etc.
        If depth is -1, the current node is unset (set to None).

        Raises:
            ValueError: If the given depth is deeper than the current node.
        """
        if depth == -1:
            self._current = None
            return

        # Build path from current to root (in reverse)
        path = []
        node = self._current
        while node:
            path.append(node)
            node = node.parent

        current_depth = len(path) - 1

        if depth > current_depth:
            raise ValueError(f"Target depth {depth} is deeper than\
                    current depth {current_depth}")

        self._current = path[current_depth - depth]

    def move_up(self):
        if not self._current:
            raise ValueError("Cannot move up, if current is unassigned")

        self._current = self._current.parent
        # the case parent == None does not require special handling

    def add_child(self, obj):
        """
        Add a new parsed object as a child of the current node.

        The new node becomes the current node.
        """

        if self._current is None:
            # No current node: treat as top-level root
            self._root_nodes.append(obj)
        else:
            self._current.add_child(obj)

        self._current = obj

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
            print(f"{prefix}- {type(node).__name__}")
            for child in node.get_children():
                walk(child, depth + 1)

        for root in self._root_nodes:
            walk(root, 0)

