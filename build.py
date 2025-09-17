from datetime import datetime
import sys
import time
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pathlib import Path
from compiler import HTMLCompiler


def write_index_html(post: str, output_path: str) -> None:
    # Erases contents of index.html
    open(output_path, "w").close()
    with open(output_path, "a") as index_html:
        index_html.write("<!DOCTYPE html>\n")

        # Write header.html to index.html
        with open("header.html", "r") as f:
            if HAS_KATEX:
                header_html = f.read()
                i = header_html.find("</script>\n") + 10
                index_html.write(
                    header_html[:i]
                    + """
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
                """
                    + header_html[i:]
                )
            else:
                index_html.write(f.read())

        index_html.write("<body>\n")
        index_html.write("\t<main>\n")
        index_html.write("\t\t<nav>\n")
        index_html.write("This is the navigation bar")
        index_html.write("\t\t</nav>\n")
        index_html.write("\t\t<article>\n")
        # Write post contents
        index_html.write(post)

        today_date = datetime.today().strftime("%Y-%m-%d")

        index_html.write("\t\t</article>\n")
        index_html.write("<br><br>\n\t</main>\n")
        # Write footer
        with open("footer.html", "r") as footer_html:
            index_html.write(footer_html.read().format(date=today_date))


def compile(post_name: str) -> None:
    # Create folder for index.html to sit in if it doesn't already exist
    Path("results/" + post_name).mkdir(parents=True, exist_ok=True)
    with open("posts/" + post_name + ".md", "r") as f:
        html_compiler = HTMLCompiler(f)
        ugly_html = html_compiler.compile()
        write_index_html(ugly_html, "results/" + post_name + "/index.html")


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent) -> None:
        modified_file_name = event.src_path.split("/")[-1][:-3]
        compile(modified_file_name)
        print(f"{modified_file_name}.md has been updated")


def has_arg_flag(flag: str) -> bool:
    return any(sys.argv[i] == flag for i in range(len(sys.argv)))


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
        post_name = post.split("/")[-1][
            :-3
        ]  # remove .md extension and folder from file name
        print('Compiling post "' + post_name + '"')
        compile(post_name)

    print("Posts converted successfully! Now observing changes...")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path="posts/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
