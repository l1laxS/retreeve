from retreeve import Parser, BaseHandler, NO_MATCH_REGEX
from io import StringIO
import re


class SolHandler(BaseHandler):
    first_line_re = re.compile(r"^SOL")
    feed_line_re = NO_MATCH_REGEX


class ExecControlHandler(BaseHandler):
    first_line_re = re.compile(r"^CEND")
    feed_line_re = NO_MATCH_REGEX


class CommentHandler(BaseHandler):
    first_line_re = re.compile(r"^$")
    feed_line_re = re.compile(r"^$")


class CardHandler(BaseHandler):
    first_line_re = re.compile(r"^\w")
    feed_line_re = re.compile(r"^\+")


class BulkHandler(BaseHandler):
    first_line_re = re.compile(r"^BEGIN BULK")
    feed_line_re = re.compile(r"^ENDDATA")
    subhandlers = [CardHandler, CommentHandler]


handlers = [SolHandler, ExecControlHandler, BulkHandler]


def run_example():
    txt = open("examples/nastran/input.txt").read()
    parser = Parser(handlers)
    with StringIO(txt) as stream:
        parser.parse(stream)
    return parser.parsed_obj._root_nodes
