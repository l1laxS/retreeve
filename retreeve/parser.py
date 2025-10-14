from typing import TextIO
from .handlers.special import SpecialHandler


class Parser:
    def __init__(self, handlers: list):
        self.handler = SpecialHandler(handlers)

    def parse(self, stream: TextIO):
        self.handler.parse(stream)

    def get_dict(self):
        return self.handler.__repr__()
