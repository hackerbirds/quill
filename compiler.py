from enum import Enum
from html import escape
import re
from macros import LINE_FORMAT, INLINE_FORMAT


class TextMode(Enum):
    REGULAR = 1
    CODE_BLOCK = 2
    UNORDERED_LIST = 3
    ORDERED_LIST = 4
    RAW_HTML = 5


class HTMLCompiler:
    def __init__(self, md_file: str) -> None:
        self.mdFile = md_file
        self.html = ""
        self.state = TextMode.REGULAR

    def parse_inline(self, line: str) -> str:
        for c, html_tag in INLINE_FORMAT.items():
            # Number of times `c` has been replaced
            i = 0
            while c in line:
                if i % 2 == 0:
                    line = line.replace(c, f"<{html_tag}>", 1)
                else:
                    line = line.replace(c, f"</{html_tag}>", 1)

                i += 1

        line = line.replace("\\star", "*")
        line = line.replace("\\tick", "`")

        return line

    def parse_line(self, line: str) -> str:
        escaped_line = escape(line)
        for reg, exp in LINE_FORMAT.items():
            formatted_line = exp
            search = re.search(reg, escaped_line)
            if search is not None:
                for i, group in enumerate(search.groups()[1:]):
                    formatted_line = formatted_line.replace(
                        "{" + f"{i}" + "}", self.parse_inline(group).rstrip()
                    )
                return formatted_line

        # Nothing was to be formatted, so we default to a paragraph
        return "<p>" + self.parse_inline(escaped_line).rstrip() + "</p>\n"

    def compile(self) -> str:
        for line in self.mdFile:
            match self.state:
                case TextMode.CODE_BLOCK:
                    if line == "```\n":
                        self.state = TextMode.REGULAR
                        self.html += "</pre>\n"
                    else:
                        self.html += line
                case TextMode.RAW_HTML:
                    if line == "<>\n":
                        self.state = TextMode.REGULAR
                    else:
                        self.html += line
                case TextMode.UNORDERED_LIST:
                    if line.startswith("* "):
                        self.html += self.parse_line(line)
                    else:
                        self.state = TextMode.REGULAR
                        self.html += "</ul>\n"
                case TextMode.ORDERED_LIST:
                    if line.startswith("*) "):
                        self.html += self.parse_line(line)
                    else:
                        self.state = TextMode.REGULAR
                        self.html += "</ol>\n"
                case _:
                    # If in regular state, check if we enter new state
                    if line == "```\n":
                        # Enter code block state
                        self.state = TextMode.CODE_BLOCK
                        self.html += '<pre aria-label="">\n'
                    elif line == "<>\n":
                        self.state = TextMode.RAW_HTML
                    elif line.startswith("* "):
                        self.state = TextMode.UNORDERED_LIST
                        self.html += "<ul>\n"
                        self.html += self.parse_line(line)
                    elif line.startswith("*) "):
                        self.state = TextMode.ORDERED_LIST
                        self.html += "<ol>\n"
                        self.html += self.parse_line(line)
                    else:
                        self.html += self.parse_line(line)

        return self.html
