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

    def parseInline(self, escaped_line):
        # This is for inline code blocks
        if "`" in escaped_line:
            split_code_line = escaped_line.split("`")
            if len(split_code_line) % 2 == 0:
                # Means there's an odd amount of '`` which shouldn't happen
                raise Exception(
                    'Code tag weirdly formatted at line "'
                    + escaped_line
                    + "\". Are you sure there is the right amount of '`' in your line?"
                )

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if "`" not in escaped_line:
                    break
                code_tick_index = escaped_line.index("`")
                if open_tag is True:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "<code>"
                        + escaped_line[code_tick_index + 1 :]
                    )
                    open_tag = False
                else:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "</code>"
                        + escaped_line[code_tick_index + 1 :]
                    )
                    open_tag = True

        # Inline italic text
        if "__" in escaped_line:
            split_code_line = escaped_line.split("__")
            if len(split_code_line) % 2 == 0:
                raise Exception(
                    'Italics formatted at line "'
                    + escaped_line
                    + "\". Are you sure there is the right amount of '__' in your line?"
                )

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if "__" not in escaped_line:
                    break
                code_tick_index = escaped_line.index("__")
                if open_tag is True:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "<i>"
                        + escaped_line[code_tick_index + 2 :]
                    )
                    open_tag = False
                else:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "</i>"
                        + escaped_line[code_tick_index + 2 :]
                    )
                    open_tag = True
        # Inline bold text
        if "*" in escaped_line:
            split_code_line = escaped_line.split("*")
            if len(split_code_line) % 2 == 0:
                raise Exception(
                    'Bold formatted at line "'
                    + escaped_line
                    + "\". Are you sure there is the right amount of '*' in your line?"
                )

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if "*" not in escaped_line:
                    break
                code_tick_index = escaped_line.index("*")
                if open_tag is True:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "<b>"
                        + escaped_line[code_tick_index + 1 :]
                    )
                    open_tag = False
                else:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "</b>"
                        + escaped_line[code_tick_index + 1 :]
                    )
                    open_tag = True
        # Inline strikethrough text
        if "~~" in escaped_line:
            split_code_line = escaped_line.split("~~")
            if len(split_code_line) % 2 == 0:
                raise Exception(
                    'Strikethrough formatted at line "'
                    + escaped_line
                    + "\". Are you sure there is the right amount of '~~' in your line?"
                )

            open_tag = True
            # For loop for all the `
            for thing in split_code_line:
                # Actually the loop goes one extra round so
                # we need this if condition for when there are no more `
                if "~~" not in escaped_line:
                    break
                code_tick_index = escaped_line.index("~~")
                if open_tag is True:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "<s>"
                        + escaped_line[code_tick_index + 2 :]
                    )
                    open_tag = False
                else:
                    escaped_line = (
                        escaped_line[:code_tick_index]
                        + "</s>"
                        + escaped_line[code_tick_index + 2 :]
                    )
                    open_tag = True

        escaped_line = escaped_line.replace("\\star", "*")
        escaped_line = escaped_line.replace("\\tick", "`")

        return escaped_line

    def parseLine(self, line):
        escaped_line = escape(line)
        for reg, exp in FORMAT_OPTIONS.items():
            formatted_line = exp
            search = re.search(reg, escaped_line)
            if search is not None:
                for i, group in enumerate(search.groups()[1:]):
                    formatted_line = formatted_line.replace(
                        "{" + f"{i}" + "}", self.parseInline(group).rstrip()
                    )
                return formatted_line

        # Nothing was to be formatted, so we default to a paragraph
        return "<p>" + self.parseInline(escaped_line).rstrip() + "</p>\n"

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
