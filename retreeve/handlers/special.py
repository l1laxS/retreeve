from .base import BaseHandler
import re


NO_MATCH_REGEX = re.compile(r"a^")
ANY_MATCH_REGEX = re.compile(r".*")


class FallbackHandler (BaseHandler):
    first_line_re = ANY_MATCH_REGEX
    feed_line_re = NO_MATCH_REGEX  # only one line allowed


class SpecialHandler (BaseHandler):
    first_line_re = NO_MATCH_REGEX
    feed_line_re = NO_MATCH_REGEX
    _instance = None  # Class variable to store the singleton instance

    def __init__(self, handlers: list[type[BaseHandler]]):
        self.lines = list()
        self.__class__.subhandlers = handlers
        self.__class__.subhandlers.append(FallbackHandler)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpecialHandler, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return repr(self.lines)
