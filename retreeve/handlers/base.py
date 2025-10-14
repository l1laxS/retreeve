import re
from typing import TextIO, Type


class BaseHandler:
    """Abstract base class for stream-based, regex-driven multi-line handlers.
    Subclasses should define:
    - first_line_re: regex for first line
    - feed_line_re: regex for following lines or None
    - subhandlers: list of handler classes (optional)
    """
    first_line_re: re.Pattern = None
    feed_line_re: re.Pattern = None
    subhandlers: list[Type["BaseHandler"]] = []

    def __init__(self, line):
        self.lines = [line]

    @classmethod
    def matches(cls, line: str) -> bool:
        """Return True if this handler can start on the given line."""
        return cls.first_line_re and cls.first_line_re.match(line)

    def parse(self, stream: TextIO):
        while line := stream.readline():
            while line:
                for sub in self.__class__.subhandlers:
                    if sub.matches(line):
                        child = sub(line)
                        line = child.parse(stream)
                        self.lines.append(child)
                        break
                else:
                    if self.__class__.feed_line_re.match(line):
                        self.lines.append(line)
                        line = None
                    else:
                        return line  # give back control to the upper class

    def __repr__(self, level=0):
        indent = '  ' * level
        inner_indent = '  ' * (level + 1)

        lines = []
        for item in self.lines:
            if isinstance(item, BaseHandler):
                # Recursively call _ repr _ with increased indent level
                lines.append(item.__repr__(level+1))
            else:
                # Assume it's a string, format it with quotes
                item = item.rstrip("\n")
                lines.append(f"'{item}'")

        inner = ',\n'.join(f"{inner_indent}{line}" for line in lines)
        return f"{{ {self.__class__.__name__}: [\n{inner}]\n{indent}}}"
