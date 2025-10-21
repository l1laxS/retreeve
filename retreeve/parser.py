from typing import TextIO
from .handler_tree import HandlerTree
from .parser_tree import ParseTree
from .handlers.special import FallbackHandler


class Parser:
    """
    A line-by-line parser for hierarchical block-structured files.

    Lines are parsed by matching against a tree of handlers. If no handler
    matches and the current node can't accept the line via `.feed()`, a
    fallback handler is used to wrap the line without interpretation.
    """

    def __init__(self, handlers: list):
        self.handlers_tree = HandlerTree(handlers)
        self.parsed_obj = ParseTree()

    def parse(self, stream: TextIO):
        """Parse the input stream line by line."""
        while line := stream.readline():
            self.handle_line(line)

    def handle_line(self, line):
        """
        Handle a single line by matching handlers, feeding, or falling back.

        1. Try matching a handler in the same or higher level (breadth-first).
        2. Try matching a handler among current node's children.
        3. Try feeding the line to the current parsed object.
        4. Move up and retry.
        5. If all else fails, wrap the line with fallback and continue.
        """
        for handler, depth in self.handlers_tree.breadth_first():
            handled = handler(line)
            if handled:
                self.handlers_tree.set_current(handler)
                self.parsed_obj.move_up_to(depth - 1)
                self.parsed_obj.add_child(handled)
                return

        for handler in self.handlers_tree.current_children():
            handled = handler(line)
            if handled:
                self.handlers_tree.set_current(handler)
                self.parsed_obj.add_child(handled)
                return

        for old_handler in self.parsed_obj.current_and_ancestors():
            if old_handler.feed(line):
                self.handlers_tree.set_current(old_handler)
                self.parsed_obj.set_current(old_handler)
                return

        # Fallback always succeeds; no checks needed
        handled = FallbackHandler(line)
        # Do not change self.handler_tree._current
        self.parsed_obj.move_up()
        self.parsed_obj.add_child(handled)
        return
