import argparse
import glob
import os
import time
from datetime import datetime
from pathlib import Path

from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .compiler import HTMLCompiler


def write_index_html(
    post: str,
    output_path: str,
    header_html_path: Path,
    footer_html_path: Path,
    katex: bool,
) -> None:
    """Writes the content of the post to an index.html file."""

    # Erases contents of index.html
    open(output_path, "w").close()
    with open(output_path, "a") as index_html:
        index_html.write("<!DOCTYPE html>\n")

        # Write header.html to index.html
        with open(header_html_path, "r") as f:
            if katex:
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
        with open(footer_html_path, "r") as footer_html:
            index_html.write(footer_html.read().format(date=today_date))


def compile(
    input_path: Path,
    name: str,
) -> None:
    global ARGS
    header_html_path = ARGS.header_html
    footer_html_path = ARGS.footer_html
    katex = ARGS.katex

    output_path = Path("results") / name / "index.html"
    print(f"Compiling {name} from path {input_path} to {output_path}")

    # Create folder for index.html to sit in if it doesn't already exist
    (Path("results") / name).mkdir(parents=True, exist_ok=True)
    with open(input_path, "r") as f:
        html_compiler = HTMLCompiler(f)
        ugly_html = html_compiler.compile()
        write_index_html(
            ugly_html, output_path, header_html_path, footer_html_path, katex
        )


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent) -> None:
        post_name = event.src_path.split("/")[-1][
            :-3
        ]  # remove .md extension and folder from file name

        compile(event.src_path, post_name)


def main() -> None:
    cwd = Path(os.getcwd())
    parser = argparse.ArgumentParser(
        prog="quill", description="Generate a static site from Markdown-style files"
    )

    parser.add_argument("-p", "--posts", default=cwd, type=Path)
    parser.add_argument(
        "-hhtml", "--header-html", default=(cwd / "header.html"), type=Path
    )
    parser.add_argument(
        "-fhtml", "--footer-html", default=(cwd / "footer.html"), type=Path
    )

    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="Watch for file changes and automatically recompile",
    )
    parser.add_argument("-k", "--katex", action="store_true", help="Include KaTeX")
    parser.add_argument(
        "-cb", "--code-block", action="store_true", help="Include code blocks"
    )

    parsed_cli_args = parser.parse_args()

    global ARGS
    ARGS = parsed_cli_args

    if ARGS.katex:
        print("Compiling with KaTeX")
    if ARGS.code_block:
        print("Compiling with formatted code blocks")

    if not parsed_cli_args.posts.is_dir():
        post_name = str(parsed_cli_args.posts)[
            :-3
        ]  # remove .md extension from file name

        compile(parsed_cli_args.posts, post_name)
    else:
        # Create folders if they don't exist already
        parsed_cli_args.posts.mkdir(parents=True, exist_ok=True)

        posts = glob.glob(str(parsed_cli_args.posts / "*.md"))
        for post_path in posts:
            post_name = post_path.split("/")[-1][
                :-3
            ]  # remove .md extension and folder from file name

            compile(post_path, post_name)

    if parsed_cli_args.watch:
        print("Watching for file changes...")
        print("To stop, end with CTRL+C")
        event_handler = FileHandler()
        observer = Observer()
        observer.schedule(event_handler, path=parsed_cli_args.posts, recursive=False)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
