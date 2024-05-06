(this is a prototype, so, not ready to use yet)  


# What is AuXML? (Author XML)

It's XML minus the namespace stuff plus a macro system.

# Why does it exist?

Two main reasons. Markdown and friends are not good for authoring large
documents and XML/HTML is painful to write. 

# What does it look like?

Suppose you are authoring a large document in HTML, and are
writing a paragraph, such as this:

```html
<p>
It was the best of times, it was the blurst of times, it
was the age of wisdom, it was the age of foolishness, it was the epoch
of belief, it was the epoch of incredulity, it was the season of
light, it was the season of darkness, it was the spring of hope, it
was the winter of despair.
</p>
```

You'd like to add some styling to part of the first sentence. To do
that, you might use a span with some CSS.

```html
<p>
  <span class="some-rule">It was the best of times, it was the blurst of times</span>,
  it was the age of wisdom ...
</p>
```

Manually typing that span just once is not too hard, but typing it
over and over again would be awful! We can do better! What if there
was a way to define a macro to make things easier? Then we could
reduce:

```html
<span class="some-rule">It was the best of times, it was the blurst of times</span>
```

down to:

```html
<some-rule>It was the best of times, it was the blurst of times</some-rule>
```

Or shorten the macro name down to just `sr`:

```html
<sr>It was the best of times, it was the blurst of times</sr>
```

OK, so what would such a macro look like? In AuXML, it looks like this:

```xml
<defmacro name="sr">
  <span class="some-rule"><contents/></span>
</defmacro>
```

That's the macro definition. To use it, invoke the macro with name
`sr` by typing:

```xml
<sr> your text goes here </sr>
```

which will replace the `<contents/>` tag found in the macro definition
and produce:

```html
<span class="some-rule"> your text goes here </span>
```

There are a few more features, but that's the gist of it.  The whole
system is roughly 700 lines of python code, lxml does all the heavy
lifting.




