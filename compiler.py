from enum import Enum
from html import escape


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
                    + line
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
        return escaped_line

    def parseLine(self, line):
        escaped_line = escape(line)
        if escaped_line == "\n":
            return "<br>\n"
        elif escaped_line.startswith("# "):
            text = escaped_line.rstrip()[2:]
            return "<h1>" + self.parseInline(text) + "</h1>\n"
        elif escaped_line.startswith("## "):
            text = escaped_line.rstrip()[3:]
            return "<h2>" + self.parseInline(text) + "</h2>\n"
        elif escaped_line.startswith("### "):
            text = escaped_line.rstrip()[4:]
            return "<h3>" + self.parseInline(text) + "</h3>\n"
        elif escaped_line.startswith("% "):
            text = escaped_line.rstrip()[2:]
            return (
                '<div class="f-v2">\n\t<div class="bird neutral"></div>\n\t<p>'
                + self.parseInline(text)
                + "</p>\n</div>\n"
            )
        elif escaped_line.startswith("-&gt; ") or escaped_line.startswith("-> "):
            if " | " in escaped_line:
                split_line = escaped_line.rstrip().split(" | ")
                url = " ".join(split_line[0].split(" ")[1:])
                text = ""
                img_quote_html = ""
                if len(split_line) > 1:  # There is text after the URL
                    text = ' alt="' + split_line[1] + '"'
                if len(split_line) > 2:  # There is a quote after the text
                    img_quote_html = "<i>" + split_line[2] + "</i>"

                return (
                    '<div class="attachment-div">\n\t<img onclick="window.open(\''
                    + url
                    + '\', \'_blank\');" class="attachment" src="'
                    + url
                    + '"'
                    + text
                    + "/>"
                    + self.parseInline(img_quote_html)
                    + "</div>\n"
                )
            else:
                split_line = escaped_line.rstrip().split(" ")
                url = split_line[1]
                text = ""
                if len(split_line) > 2:  # There is text after the URL
                    text = " ".join(split_line[2:])

                return (
                    '<img class="attachment" src="'
                    + url
                    + '" alt="'
                    + self.parseInline(text)
                    + '"/>\n'
                )
        # Link/URL (" => ")
        elif escaped_line.startswith("=&gt; ") or escaped_line.startswith("=> "):
            split_line = escaped_line.rstrip().split(" ")
            url = split_line[1]
            text = url
            if len(split_line) > 2:  # There is text after the URL
                text = " ".join(split_line[2:])

            return (
                '<a class="arrow" href="'
                + url
                + '">'
                + self.parseInline(text)
                + "</a>\n<br>\n"
            )
        # List element
        elif escaped_line.startswith("* "):
            return "\t<li>" + self.parseInline(line[2:]).rstrip() + "</li>\n"
        elif escaped_line.startswith("*) "):
            return "\t<li>" + self.parseInline(line[3:]).rstrip() + "</li>\n"
        # Blockquote (" > ")
        elif (
            escaped_line.startswith("&gt; ") and not escaped_line.startswith("=&gt; ")
        ) or (escaped_line.startswith("> ") and not escaped_line.startswith("=> ")):
            return (
                "<blockquote>\n\t<p>"
                + self.parseInline(escaped_line[4:]).rstrip()
                + "</p>\n</blockquote>\n"
            )
        # Bar line
        elif escaped_line == "---\n":
            return "<hr>\n"
        else:
            html = "<p>" + self.parseInline(escaped_line).rstrip() + "</p>\n"
            html = html.replace("\\star", "*")
            html = html.replace("\\tick", "`")
            return html

    def compile(self) -> str:
        for line in self.mdFile:
            match self.state:
                case TextMode.CODE_BLOCK:
                    if line == "```\n":
                        # Exit code block state
                        self.state = TextMode.REGULAR
                        self.html += "</pre>\n"
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
