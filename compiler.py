from enum import Enum
from html import escape
import re
from macros import FORMAT_OPTIONS


class TextMode(Enum):
    REGULAR = 1
    CODE_BLOCK = 2
    UNORDERED_LIST = 3
    ORDERED_LIST = 4
    RAW_HTML = 5


class HTMLCompiler:
    def __init__(self, mdFile):
        self.mdFile = mdFile
        self.html = ""
        self.state = TextMode.REGULAR

    def parse_inline(self, line):
        inline_characters = ["`", "__", "*", "~~"]
        for c in inline_characters:
            # Number of times `c` has been replaced
            i = 0
            while c in line:
                if i % 2 == 0:
                    match c:
                        case "`":
                            line = line.replace(c, "<code>", 1)
                        case "__":
                            line = line.replace(c, "<i>", 1)
                        case "*":
                            line = line.replace(c, "<b>", 1)
                        case "~~":
                            line = line.replace(c, "<s>", 1)
                else:
                    match c:
                        case "`":
                            line = line.replace(c, "</code>", 1)
                        case "__":
                            line = line.replace(c, "</i>", 1)
                        case "*":
                            line = line.replace(c, "</b>", 1)
                        case "~~":
                            line = line.replace(c, "</s>", 1)

                i += 1

        line = line.replace("\\star", "*")
        line = line.replace("\\tick", "`")

        return line

    def parseLine(self, line):
        escaped_line = escape(line)
        for reg, exp in FORMAT_OPTIONS.items():
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
                        # Exit code block state
                        self.state = TextMode.REGULAR
                        self.html += "</pre>\n"
                    else:
                        self.html += line
                case TextMode.RAW_HTML:
                    if line == "<>\n":
                        self.state = TextMode.REGULAR
                    else:
                        # Unparsed line (raw HTML)
                        self.html += line
                case TextMode.UNORDERED_LIST:
                    if line.startswith("* "):
                        self.html += self.parseLine(line)
                    else:
                        self.state = TextMode.REGULAR
                        self.html += "</ul>\n"
                case TextMode.ORDERED_LIST:
                    if line.startswith("*) "):
                        self.html += self.parseLine(line)
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
                        self.html += self.parseLine(line)
                    elif line.startswith("*) "):
                        self.state = TextMode.ORDERED_LIST
                        self.html += "<ol>\n"
                        self.html += self.parseLine(line)
                    else:
                        self.html += self.parseLine(line)

        return self.html
