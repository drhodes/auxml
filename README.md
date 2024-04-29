
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
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
  eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
  minim veniam, quis nostrud exercitation ullamco laboris nisi ut
  aliquip ex ea commodo consequat. 
</p>
```

You'd like to add some styling to part of the first sentence. To do
that, you might use a span with some CSS.

```html
<p>
  <span class="some-rule">Lorem ipsum dolor sit amet</span>,
  consectetur ...
</p>
```

Manually typing that span just once is not too onerous. Typing it over
and over again is awful! We can do better! What if there was a way to
define a macro to save some typing? Then we could reduce:

```html
<span class="some-rule">Lorem ipsum dolor sit amet</span>
```

down to:

```html
<some-rule>Lorem ipsum dolor sit amet</some-rule>
```

Or even:

```html
<sr>Lorem ipsum dolor sit amet</sr>
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




