# Quill (Hackerbirds's static blog page builder)

> [!NOTE]  
> This project is currently being rebuilt to be more usable for external users, with the goal
> that anyone can use and customize this for their own blog.

Write blog posts quickly using this little script. Originally based on [Lichen](https://lichen.sensorstation.co/), it is backwards compatible with Gemtext formatting.

## Installation and usage

Using `pip`, as such: `python3 -m pip install -r requirements.txt`

To write a post named `example-post`, make a file `posts/example-post.md`, write your stuff in there, then call `python3 build.py`. The script is build to stay active and automatically recompile whenever it detects a change inside `posts/*.md`.

## Features

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

## What? Why?

* https://hackerbirds.neocities.org/Slightly-Less-Worse-HTML/
* https://hackerbirds.neocities.org/new-redesign/

## Disclaimers

### This is not a fully-automated script

You are meant to manually modify the code and resulting HTML to your liking if needed.

### You are all alone in this adventure

We will not maintain or modify this project for anyone else but us. That said, if you think you can use it or modify it for yourself, go ahead.
