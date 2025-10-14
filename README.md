# ReTreeVe — Regex Tree Versatile Extractor

**ReTreeVe** (from *“retrieve”*) is a lightweight Python library for extracting structured data from plain text files, using user-defined regular expressions.  
It acts as a **Regex Tree Versatile Extractor**, building a nested tree representation of your text, based on pattern matches and logical block relationships.

With ReTreeVe, you can retrieve structure from chaos — turning any ASCII or log-like text into rich, queryable objects.

## ✨ Features
-	🧩 Regex-driven parsing — define line or block handlers using simple patterns.
-	🌳 Nested tree structure — automatically captures logical hierarchy in your text.
-	⚙️ Customizable readers — plug in your own handler functions per pattern.
-	📜 Generic ASCII support — works with any text source: logs, configs, reports, etc.
-	🪶 Lightweight & extensible — no heavy dependencies, simple API.

## 🔓 Open by Design

Unlike many parsers tailored for specific proprietary formats, **ReTreeVe** is intentionally **format-agnostic** and released under the **MIT license**.  
That means you can adapt it to your own text structures — scientific logs, simulation outputs, configuration files — and integrate it freely in both open and closed projects.

## 💡 Example

```python
from retreeve import Parser, BaseHandler, NO_MATCH_REGEX
import re


class SectionHandler(BaseHandler):
    first_line_re = re.compile(r"^Section -")
    feed_line_re = re.compile(r"^\w")


class TitleHandler(BaseHandler):
    first_line_re = re.compile(r"^TITLE: ")
    feed_line_re = NO_MATCH_REGEX # only one line allowed
    subhandlers = SectionHandler

parser = Parser([TitleHandler])
with open("myfile.txt") as f:
    parser.parse(f)

print(parser.get_dict())
```
```python
{
    "items": [
        TitleHandler(
            items=[
                "TITLE: Lorem ipsum",
                SectionHandler(
                    items=[
                        "Section - Lorem ipsum dolor sit amet, consetetur ",
                        "sadipscing elitr, sed diam nonumy eirmod tempor invidunt ",
                        "ut labore et dolore magna aliquyam erat, sed diam ",
                        "voluptua. At vero eos et accusam et justo duo dolores et ",
                        "ea rebum."
                    ]
                )
            ]
        )
    ]
}
```