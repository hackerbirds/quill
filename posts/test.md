# Creating blog posts faster with quill

(To see the text before building, see `posts/test.md`. If you want the compiled HTML, see `results/test/index.html`.)
(If you are reading this through GitHub, the markdown viewer will automatically enable. Please click "Raw" to see the raw version, this is important!!)

Creating paragraphs is easy. Just write as much as you want in one straight line, and to make a new paragraph...

Just add a new line like we just did. If you want to separate your text even more, there's always the horizontal bar:
---
Now your text is extra separate. Awesome!!!

Each new line (`\n`) is a line break in HTML, so add spaces whenever you feel like it. Here's an extra wide space for your paragraphs:




Wow, silent.

## Headers

# That's big. For the title.
## That's not as big. For main sections.
### That's even smaller. The smallest, actually. For subsections.

## Formatting

You can do a bunch of inline stuff, like *bold*, __italic__, ___underline___, or ~~strikethrough~~ text if that's what you want. __*~~why not all of them at once too?~~*__

Need to use a single \star or \tick in the middle of your text too? Write "\ star" or "\ tick" (without the space): *now\staryou\starcan\starhave\starall\starthe\starstars* 

Like this: \star \tick \star \tick \star

Do you want your text to look monospace? There's the `inline code formatting` for that.

```
Or a whole block,
  if you  need   to   paste

       anything without  formatting.
```

## Links

You can have a link like this:

=> https://hackerbirds.neocities.org/

Or modify the text to your desires:

=> https://hackerbirds.neocities.org/ Visit our blog

## Images

To add an image (for accessibility reasons you must add alt text), here's how you do it:

-> ./dinosaurs.jpeg | Photo of adorable dinosaurs

And if you want text under your image, add another parameter like such:

-> ./dinosaurs.jpeg | Photo of adorable dinosaurs | Aren't they cute?

## Lists

Lists automatically start when you add an element and end when you make an empty new line, like this:

* This is an unordered list.
* Unordered means the elements aren't numbered.
* To add elements, just start the line with `"\star "`.

*) This is an *ordered* list.
*) Ordered means the elements are numbered.
*) To add elements, just start the line with `"\star) "`.

## Do you like the hackerbird dialog blocks?

% Lucky for us, it's just an `%` away.

## HTML Block

If all of these features aren't enough for you, and you need extra customisation, the HTML block is for you:

<>
<p style="color: blue; background-color: black; padding: 6px;">
Anything between the "<>" will be processed as raw HTML.
</p>
<>

For instance, you could use it for <details> as such:

<>
<details>
<summary>Click here to see more stuff!</summary>
Boop! Hello!
</details>
<>

It is far from perfect but we hope you will find our tool convenient.