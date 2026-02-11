# Quill

With Quill, you can write a static site quickly, starting from Markdown-style text. It is designed mainly for blog posts (since it was created for [ours](https://hackerbirds.neocities.org)). 

Quill is easily extensible, so you can add new features for your Markdown. Changes in your Markdown files will automatically be recompiled. Inspired by [Lichen](https://lichen.sensorstation.co/), it also makes use of Gemtext formatting.

## Installation and usage

Using `uv`, you can run the build script with `uv run build.py`. While the build script is running, any modifications you make under `posts/*.md` will automatically compile into `results/*/index.html`.

<details>
<summary><h2>How to use</h2></summary>

Below are examples for each of the features. 

### You may also check at `posts/test.md` and the resulting html file in `results/test/index.html` to see how it looks in practice.

#### Inline text formatting
* Bold text: `Wrap the text with a star (*). Example: *this text will be bold*`
* Italic text: `Wrap the text with two underscores (__). Example: __this text will be italic__`
* Strikethrough text: `Wrap the text with two tildes (~~). Example: ~~this text will be strikethoughd~~`

#### Title and headers

* `# Title`
* `## Big header`
* `### Smaller header`

#### Code

* Inline code/monospace font: ````Wrap the text with two ticks (`). Example: `this will be monospace`.````
* Code blocks/monospace blocks:
````
Wrap the text with three ticks *in new lines* to start the code block.
Make sure the lines with the ticks does not contain any text.

Example:

```
this is a code block!
```
````

#### Unordered lists

````
How to make an unordered list:
* Make a list
* Like this
* One list element per line
* Add a star for each element in the list
````

#### Ordered lists

````
How to make an ordered list:
*) Make a list
*) Like this
*) One list element per line
*) Add a star and a closing parenthesis for each element in the list
````

#### Images (with optional text below)
````
How to add an image:

With no text below:
-> path/to/your/image.png | This is some alt text

With text below:
-> path/to/your/image.png | This is some alt text | Optionally, you can add visible text below the image
````

#### Block quotes
````
To make a block quote, add a new line and start it with "> " (don't forget the space). Anything after will be part of the quote.

> This is a very serious quote.
````

#### URL/Links

````
Links are similar looking to images, so be careful to not confuse between them!

=> https://zombo.com You can do anything at Zombo.com
````

#### Hackerbirds's signature bird dialogue block

````
% If you write a line starting with "%" like this, a little bird will show up next to your gorgeous text.
````

#### Horizontal bar break:
````
To add an horizontal bar to break off your paragraphs,
you can add a line consisting of three consecutive dashes ("---")
Like so:
---
Now, this text is separated and alone.
````

#### Raw HTML Block:

````
<>
<!-- anything between the <> is raw HTML. -->
<p style="color: red;">Hello!</p>
<>
````

</details>