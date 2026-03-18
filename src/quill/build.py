from datetime import datetime
from pathlib import Path
from .compiler import HTMLCompiler

def write_index_html(post: str, output_path: str, katex: bool) -> None:
    # Erases contents of index.html
    open(output_path, "w").close()
    with open(output_path, "a") as index_html:
        index_html.write("<!DOCTYPE html>\n")

        # Write header.html to index.html
        with open("header.html", "r") as f:
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
        with open("footer.html", "r") as footer_html:
            index_html.write(footer_html.read().format(date=today_date))

def compile(post_path: str, katex: bool) -> None:
    post_name = post_path.split("/")[-1][
        :-3
    ]  # remove .md extension and folder from file name

    print(f"Compiling {post_name}")

    # Create folder for index.html to sit in if it doesn't already exist
    Path("results/" + post_name).mkdir(parents=True, exist_ok=True)
    with open(post_path, "r") as f:
        html_compiler = HTMLCompiler(f)
        ugly_html = html_compiler.compile()
        write_index_html(ugly_html, "results/" + post_name + "/index.html", katex)
