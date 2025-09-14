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
from compiler import HTMLCompiler

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
        index_html.write("<main>\n")

        # Write post contents
        index_html.write(post)

        today_date = datetime.today().strftime('%Y-%m-%d')

        index_html.write("<br><br>\n</main>")
        # Write footer
        with open("footer.html", "r") as footer_html:
            index_html.write(footer_html.read().format(date=today_date))

def compile(post_name):
    # Create folder for index.html to sit in if it doesn't already exist
    Path("results/"+postName).mkdir(parents=True, exist_ok=True)
    global HAS_CODE_BLOCK
    with open("posts/"+post_name+".md", "r") as f:
        ugly_html = HTMLCompiler(f).compile()
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
