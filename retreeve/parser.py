from typing import TextIO
from .handler_tree import HandlerTree
from .parser_tree import ParseTree


class Parser:
    def __init__(self, handlers: list):
        self.handlers_tree = HandlerTree(handlers)
        self.parsed_obj = ParseTree([])

    def parse(self, stream: TextIO):
        while line := stream.readline():
            self.handle_line(line)

    def handle_line(self, line):
        while True:
            # look for new handler in parents and sibilings
            for handler in self.handlers_tree.breadth_first():
                handled = handler(line)
                if handled:
                    self.parsed_obj.add_sibiling(handled)  # ??
                    return

            # look for new handler in children
            for handler in self.handlers_tree.current_children():
                handled = handler(line)
                if handled:
                    self.parsed_obj.add_child(handled)
                    return

            # try current handler
            if self.parsed_obj.get_current().feed(line):
                return

            self.handlers_tree.move_current_up()
            self.parsed_obj.move_current_up()

    def get_dict(self):
        pass
        # return self.handler.__repr__()
