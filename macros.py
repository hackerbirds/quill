FORMAT_OPTIONS = {
    # Empty line: line break
    r"^(\n)$": "<br>\n",
    # "---": horizontal bar break
    r"^(---\n)$": "<hr>\n",
    # "# header": h1 header
    r"^(# (?P<line>.*)\n)$": "<h1>{0}</h1>\n",
    # "## tinier header": h2 header
    r"^(## (?P<line>.*)\n)$": "<h2>{0}</h2>\n",
    # "### super tiny header": h3 header
    r"^(### (?P<line>.*)\n)$": "<h3>{0}</h3>\n",
    # "> That's how it is on this bitch on an earth": blockquote
    r"^(> (?P<quote>.*)\n)$": "<blockquote>{0}</blockquote>\n",
    # "* list element"
    r"^(\*\)? (?P<line>.*)\n)$": "<li>{0}</li>\n",
    # "*) ordered list element"
    r"^(\% (?P<quote>.*)\n)$": """<div class="f-v2">\n\t<div class="bird neutral"></div>\n\t<p>{0}</p>\n</div>\n""",
    # "-> https://thing.com/image.jpg | This is an alt text.": for images
    r"^(-&gt; (?P<url>[^\s^|]+) \| (?P<alt>[^|]+)\n)$": """<div class="attachment-div">
                <img 
                    onclick="window.open('{0}', '_blank');" 
                    class="attachment" 
                    src="{0}"
                    alt="{1}"
                />
            </div>\n""",
    # "-> https://thing.com/image.jpg | This is an alt text. | And text under the image.": for images with text
    r"^(-&gt; (?P<url>[^\s^|]+) \| (?P<alt>[^|]+) \| (?P<text>.*)\n)$": """<div class="attachment-div">
                <img 
                    onclick="window.open('{0}', '_blank');" 
                    class="attachment" 
                    src="{0}"
                    alt="{1}"
                />
                <i>{2}</i>
            </div>\n""",
    # "=> https://thing.com/site": for links
    r"^(=&gt; (?P<url>[^\s]+)\n)$": """<a class="arrow" href="{0}">{0}</a><br>\n""",
    # "=> https://thing.com/site | With text to href link": for links as custom text
    r"^(=&gt; (?P<url>[^\s]+) (?P<text>.*)\n)$": """<a class="arrow" href="{0}">{1}</a><br>\n""",
}
