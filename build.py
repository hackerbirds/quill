from html import escape
from datetime import datetime
import sys
import time
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from pygments import highlight
from pygments.lexers import RustLexer
from pygments.formatters import HtmlFormatter

def parse_inline(escaped_line):
    # This is for inline code blocks
    if '`' in escaped_line:
        split_code_line = escaped_line.split("`")
        if len(split_code_line) % 2 == 0:
            # Means there's an odd amount of '`` which shouldn't happen
            raise Exception("Code tag weirdly formatted at line \""+escaped_line+"\". Are you sure there is the right amount of '`' in your line?")

        open_tag = True
        # For loop for all the `
        for thing in split_code_line:
            # Actually the loop goes one extra round so
            # we need this if condition for when there are no more `
            if '`' not in escaped_line:
                break
            code_tick_index = escaped_line.index('`')
            if open_tag is True:
                escaped_line = escaped_line[:code_tick_index] + "<code>" + escaped_line[code_tick_index+1:]
                open_tag = False
            else: 
                escaped_line = escaped_line[:code_tick_index] + "</code>" + escaped_line[code_tick_index+1:]
                open_tag = True

    # Inline italic text
    if '__' in escaped_line:
        split_code_line = escaped_line.split("__")
        if len(split_code_line) % 2 == 0:
            raise Exception("Italics formatted at line \""+escaped_line+"\". Are you sure there is the right amount of '__' in your line?")

        open_tag = True
        # For loop for all the `
        for thing in split_code_line:
            # Actually the loop goes one extra round so
            # we need this if condition for when there are no more `
            if '__' not in escaped_line:
                break
            code_tick_index = escaped_line.index('__')
            if open_tag is True:
                escaped_line = escaped_line[:code_tick_index] + "<i>" + escaped_line[code_tick_index+2:]
                open_tag = False
            else: 
                escaped_line = escaped_line[:code_tick_index] + "</i>" + escaped_line[code_tick_index+2:]
                open_tag = True
    # Inline bold text
    if ('*' in escaped_line):
        split_code_line = escaped_line.split("*")
        if len(split_code_line) % 2 == 0:
            raise Exception("Bold formatted at line \""+escaped_line+"\". Are you sure there is the right amount of '*' in your line?")

        open_tag = True
        # For loop for all the `
        for thing in split_code_line:
            # Actually the loop goes one extra round so
            # we need this if condition for when there are no more `
            if '*' not in escaped_line:
                break
            code_tick_index = escaped_line.index('*')
            if open_tag is True:
                escaped_line = escaped_line[:code_tick_index] + "<b>" + escaped_line[code_tick_index+1:]
                open_tag = False
            else: 
                escaped_line = escaped_line[:code_tick_index] + "</b>" + escaped_line[code_tick_index+1:]
                open_tag = True
    # Inline strikethrough text
    if ('~~' in escaped_line):
        split_code_line = escaped_line.split("~~")
        if len(split_code_line) % 2 == 0:
            raise Exception("Strikethrough formatted at line \""+line+"\". Are you sure there is the right amount of '~~' in your line?")

        open_tag = True
        # For loop for all the `
        for thing in split_code_line:
            # Actually the loop goes one extra round so
            # we need this if condition for when there are no more `
            if "~~" not in escaped_line:
                break
            code_tick_index = escaped_line.index("~~")
            if open_tag is True:
                escaped_line = escaped_line[:code_tick_index] + "<s>" + escaped_line[code_tick_index+2:]
                open_tag = False
            else: 
                escaped_line = escaped_line[:code_tick_index] + "</s>" + escaped_line[code_tick_index+2:]
                open_tag = True
    return escaped_line


# Parses each line into html.
def parse(line):
    html = ""
    escaped_line = escape(line)
    if escaped_line == "\n":
        return "<br>"
    else:
        # Headers: id is used to scroll
        if escaped_line.startswith("# "):
            text = escaped_line.rstrip()[2:]
            html = "<h1>"+parse_inline(text)+"</h1>"
        elif escaped_line.startswith("## "):
            text = escaped_line.rstrip()[3:]
            html = "<h2>"+parse_inline(text)+"</h2>"
        elif escaped_line.startswith("### "):
            text = escaped_line.rstrip()[4:]
            html = "<h3>"+parse_inline(text)+"</h3>"
        elif escaped_line.startswith("% "):
            text = escaped_line.rstrip()[2:]
            html = "<div class=\"f-v2\"><div class=\"bird neutral\"></div><p>"+parse_inline(text)+"</p></div>"
        elif escaped_line.startswith("-&gt; ") or escaped_line.startswith("-> "):
            if " | " in escaped_line:
                split_line = escaped_line.rstrip().split(" | ")
                url = ' '.join(split_line[0].split(' ')[1:])
                text = ""
                img_quote_html = ""
                if len(split_line) > 1: # There is text after the URL
                    text = " alt=\""+split_line[1]+"\""
                if len(split_line) > 2: # There is a quote after the text
                    img_quote_html = "<i>"+split_line[2]+"</i>"

                html = "<div class=\"attachment-div\"><img onclick=\"window.open(\'"+url+"\', \'_blank\');\" class=\"attachment\" src=\""+url+"\""+text+"/>"+parse_inline(img_quote_html)+"</div>"
            else: 
                split_line = escaped_line.rstrip().split(" ")
                url = split_line[1]
                text = ""
                if len(split_line) > 2: # There is text after the URL
                    text = ' '.join(split_line[2:])

                html = "<img class=\"attachment\" src=\""+url+"\" alt=\""+parse_inline(text)+"\"/>"
        # Link/URL (" => ")
        elif escaped_line.startswith("=&gt; ") or escaped_line.startswith("=> "):
            split_line = escaped_line.rstrip().split(" ")
            url = split_line[1]
            text = url
            if len(split_line) > 2: # There is text after the URL
                text = ' '.join(split_line[2:])

            html = "<a class=\"arrow\" href=\""+url+"\">"+parse_inline(text)+"</a><br>"
        # List element
        elif escaped_line.startswith("* "):
            html = "<li>"+parse_inline(line[2:]).rstrip()+"</li>"
        elif escaped_line.startswith("*) "):
            html = "<li>"+parse_inline(line[3:]).rstrip()+"</li>"
        # Blockquote (" > ")
        elif (escaped_line.startswith("&gt; ") and not escaped_line.startswith("=&gt; ")) or (escaped_line.startswith("> ") and not escaped_line.startswith("=> ")):
            html = "<blockquote><p>"+parse_inline(escaped_line[4:]).rstrip()+"</p></blockquote>"
        # Bar line
        elif escaped_line == "---\n":
            html = "<hr>"
        else:
            html = "<p>"+parse_inline(escaped_line).rstrip()+"</p>"
            html = html.replace("\star", "*")
            html = html.replace("\\tick", "`")
    return html

def write_index_html(post, output_path):
    # Erases contents of index.html
    open(output_path, "w").close()
    with open(output_path, "a") as index_html:
        index_html.write("<!DOCTYPE html>")
        
        # Write header.html to index.html
        with open("header.html", "r") as header_html:
            if HAS_KATEX:
                header_html = header_html.read()
                i = header_html.find('</script>\n') + 10
                index_html.write(header_html[:i] + """
                <link rel="stylesheet" href="../assets/katex/katex.min.css">
                <script defer src="../assets/katex/katex.min.js"></script>
                <script defer src="../assets/katex/contrib/auto-render.min.js"></script>
                <script>
                    document.addEventListener("DOMContentLoaded", function () {
                        renderMathInElement(document.body, {
                            delimiters: [
                                { left: '$$', right: '$$', display: true },
                                { left: '$', right: '$', display: false },
                                { left: '\\(', right: '\\)', display: false },
                                { left: '\\[', right: '\\]', display: true }
                            ],
                            throwOnError: false
                        });
                    });
                </script>
                """ + header_html[i:])
            else:
                index_html.write(header_html.read())

        index_html.write("""
            <body>
            <div class="banner" id="banner-id">
                <a href="../" title="Homepage">
                    <img src="../assets/bird_neutral.svg" class="banner-logo" alt="Main page" />
                </a>
                <b>birdbrained</b>
            </div>
        """)
        index_html.write("<main>")

        # Write post contents
        index_html.write(post)

        today_date = datetime.today().strftime('%Y-%m-%d')

        index_html.write("<br><br></main>")
        # Write footer
        with open("footer.html", "r") as footer_html:
            index_html.write(footer_html.read().format(date=today_date))

def build(post_name):
    global HAS_CODE_BLOCK
    with open("posts/"+post_name+".md", "r") as f:
        html = ""
        is_in_rust_code_block = False
        is_in_code_block = False
        is_in_html_block = False
        is_in_list = False
        is_in_ordered_list = False
        code_block = ""
        if HAS_CODE_BLOCK or is_in_rust_code_block:
            html += "<style>"+HtmlFormatter(style="lightbulb").get_style_defs('.highlight')+"</style>"
        for line in f:
            # Beginning OR end of a code block
            if line == "```\n":
                if is_in_code_block is True:
                    is_in_code_block = False
                    # Close code bock
                    html += "</pre>"
                elif is_in_rust_code_block is True:
                    # Write code block
                    html += highlight(code_block, RustLexer(), HtmlFormatter())
                    code_block = ""
                    is_in_rust_code_block = False
                else:
                    is_in_code_block = True
                    # Open code block
                    html += "<pre aria-label=\"\">"
            elif HAS_CODE_BLOCK and line == "```rust\n":
                if is_in_rust_code_block is not True:
                    is_in_rust_code_block = True
            # Beginning OR end of an HTML block
            elif line.startswith("<>"):
                if is_in_html_block is True:
                    is_in_html_block = False
                else:
                    is_in_html_block = True
            # List element
            elif line.startswith("* "):
                # If not in a list already, put us in list mode
                if is_in_list is False:
                    html += "<ul>"
                    is_in_list = True
                html += parse(line)
            elif line.startswith("*) "):
                # If not in a list already, put us in list mode
                if is_in_ordered_list is False:
                    html += "<ol>"
                    is_in_ordered_list = True
                html += parse(line)
            else:
                # Line isn't ``` (code block) or starts with "*" (list)
                if is_in_html_block is True:
                    html += line
                elif is_in_code_block is True:
                    html += escape(line)
                elif is_in_rust_code_block is True:
                    code_block += line
                elif is_in_list is True:
                    html += "</ul>"
                    html += parse(line)
                    # We exit list mode
                    is_in_list = False
                elif is_in_ordered_list is True:
                    html += "</ol>"
                    html += parse(line)
                    # We exit ordered list mode
                    is_in_ordered_list = False
                else:
                    html += parse(line)

        return html

def compile(post_name):
    # Create folder for index.html to sit in if it doesn't already exist
    Path("results/"+postName).mkdir(parents=True, exist_ok=True)
    ugly_html = build(post_name)
    write_index_html(ugly_html, "results/"+post_name+"/index.html")


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):

        modifiedFileName = event.src_path.split("/")[-1][:-3]
        compile(modifiedFileName)
        print(f"{modifiedFileName}.md has been updated")

def has_arg_flag(flag):
        for i in range(len(sys.argv)):
            if (sys.argv[i] == flag):
                return True
        return False

if __name__ == "__main__":
    HAS_CODE_BLOCK = has_arg_flag("--code-block")
    HAS_KATEX = has_arg_flag("--katex")
    posts = glob.glob("posts/*.md")
    
    if HAS_KATEX:
        print("Compiling with KaTeX")
    if HAS_CODE_BLOCK:
        print("Compiling with formatted code blocks")
    
    # Create folders if they don't exist already
    Path("posts/").mkdir(parents=True, exist_ok=True)

    for post in posts:
        postName = post.split("/")[-1][:-3] # remove .md extension and folder from file name
        print("Compiling post \""+postName+"\"")
        compile(postName)
    
    print("Posts converted successfully! Now observing changes...")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='posts/', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
