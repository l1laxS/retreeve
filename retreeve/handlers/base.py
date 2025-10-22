import re
from typing import Type, Iterable
from ..handler_tree import Node


class String:
    def __init__(self, text):
        self.text = text.rstrip("\n")

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"String({self.text!r})"


class BaseHandler(Node):
    """Abstract base class for stream-based, regex-driven multi-line handlers.
    Subclasses should define:
    - first_line_re: regex for first line
    - feed_line_re: regex for following lines or None
    - subhandlers: list of handler classes (optional)
    """
    first_line_re: re.Pattern | None = None
    feed_line_re: re.Pattern | None = None
    subhandlers: list[Type["BaseHandler"]] = []

    def __init__(self, line):
        self.parent = None
        self._contents = [String(line)]

    @classmethod
    def matches(cls, line: str) -> bool:
        """Return True if this handler can start on the given line."""
        return bool(cls.first_line_re and cls.first_line_re.match(line))

    @classmethod
    def get_children(cls) -> Iterable[Type[Node]]:
        return cls.subhandlers

    def feed_matches(self, line: str) -> bool:
        """Return True if this handler can start on the given line."""
        return bool(self.__class__.feed_line_re and
                    self.__class__.feed_line_re.match(line))

    def feed(self, line):
        self._contents.append(String(line))

    def add_child(self, child):
        child.parent = self
        self._contents.append(child)

    def __repr__(self, level=0):
        indent = '  ' * level
        inner_indent = '  ' * (level + 1)

        lines = []
        for item in self._contents:
            if isinstance(item, BaseHandler):
                # Recursively call _ repr _ with increased indent level
                lines.append(item.__repr__(level+1))
            else:
                # Assume it's a string, format it with quotes
                lines.append(item)

        inner = ',\n'.join(f"{inner_indent}{line}" for line in lines)
        return f"{{ {self.__class__.__name__}: [\n{inner}]\n{indent}}}"

    def __iter__(self):
        for item in self._contents:
            yield item
