import sys
import time
import glob
import os
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pathlib import Path
from .build import compile

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event: FileModifiedEvent) -> None:
        modified_file_name = event.src_path.split("/")[-1][:-3]

        global HAS_KATEX
        compile(modified_file_name, HAS_KATEX)
        print(f"{time.asctime()} - {modified_file_name}.md has been recompiled")


def has_arg_flag(flag: str) -> bool:
    return any(sys.argv[i] == flag for i in range(len(sys.argv)))

def main() -> None:
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(
            prog='quill',
            description='Generate a static site from Markdown-style files')

    parser.add_argument('-p', '--posts', default=f"{cwd}", type=Path)

    parser.add_argument('-w', '--watch',
        action="store_true",
        help="Watch for file changes and automatically recompile")
    parser.add_argument('-k', '--katex',
        action="store_true",
        help="Include KaTeX")
    parser.add_argument('-cb', '--code-block',
        action="store_true",
        help="Include code blocks")

    parsed_cli_args = parser.parse_args()

    global HAS_KATEX, HAS_CODE_BLOCK
    HAS_CODE_BLOCK = parsed_cli_args.code_block
    HAS_KATEX = parsed_cli_args.katex
    posts = glob.glob(str(parsed_cli_args.posts / "*.md"))

    if HAS_KATEX:
        print("Compiling with KaTeX")
    if HAS_CODE_BLOCK:
        print("Compiling with formatted code blocks")

    # Create folders if they don't exist already
    Path("posts/").mkdir(parents=True, exist_ok=True)

    for post_path in posts:
        compile(post_path, HAS_KATEX)

    print("Initial compilation completed! Now observing future changes...")
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
