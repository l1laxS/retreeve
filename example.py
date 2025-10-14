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


txt = """TITLE: Lorem Ipsum
Section - Lorem ipsum dolor sit amet, consetetur 
sadipscing elitr, sed diam nonumy eirmod tempor invidunt 
ut labore et dolore magna aliquyam erat, sed diam 
voluptua. At vero eos et accusam et justo duo dolores et 
ea rebum."""

parser = Parser([TitleHandler])
with StringIO(txt) as stream:
    parser.parse(stream)

print(parser.get_dict())
