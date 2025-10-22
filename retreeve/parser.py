from typing import TextIO
from .handler_tree import HandlerTree
from .parser_tree import ParseTree
from .handlers.special import FallbackHandler
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # or INFO in production

# Optional basic configuration if not configured elsewhere
if not logger.hasHandlers():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )


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
        logger.debug(f"Handling line: {line!r}")
        for handler, depth in self.handlers_tree.breadth_first():
            if handler.matches(line):
                logger.debug("Matched handler (breadth-first):" +
                             f"{handler} at depth {depth}")
                handled = handler(line)
                self.handlers_tree.set_current(handler)
                self.parsed_obj.move_up_to(depth - 1)
                self.parsed_obj.add_child(handled)
                logger.debug("Handler applied and parsed object updated.")
                return

        for handler in self.handlers_tree.current_children():
            if handler.matches(line):
                logger.debug(f"Matched child handler: {handler}")
                handled = handler(line)
                self.handlers_tree.set_current(handler)
                self.parsed_obj.add_child(handled)
                logger.debug("Child handler applied and parsed object " +
                             "updated.")
                return

        for old_handler in self.parsed_obj.current_and_ancestors():
            if old_handler.feed_matches(line):
                logger.debug("Feeding line to existing handler: " +
                             f"{old_handler}")
                old_handler.feed(line)
                self.handlers_tree.set_current(old_handler)
                self.parsed_obj.set_current(old_handler)
                logger.debug("Line fed to existing handler.")
                return

        # Fallback always succeeds; no checks needed
        logger.debug("No handler matched. Using FallbackHandler.")
        handled = FallbackHandler(line)
        # Do not change self.handler_tree._current
        self.parsed_obj.move_up()
        self.parsed_obj.add_child(handled)
        logger.debug("Fallback handler applied and parsed object updated.")
        return
