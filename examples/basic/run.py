from retreeve import Parser, BaseHandler, NO_MATCH_REGEX
from io import StringIO
import re


class SectionHandler(BaseHandler):
    first_line_re = re.compile(r"^Section -")
    feed_line_re = re.compile(r"^\w")


class TitleHandler(BaseHandler):
    first_line_re = re.compile(r"^TITLE: ")
    feed_line_re = NO_MATCH_REGEX  # only one line allowed
    subhandlers = [SectionHandler]


def run_example():
    txt = open("examples/basic/input.txt").read()
    parser = Parser([TitleHandler])
    with StringIO(txt) as stream:
        parser.parse(stream)
    return parser.parsed_obj._root_nodes
