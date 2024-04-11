
Processing Phases

Phase1, ensure user document is well-formed xml
Prase2, expand the macros.



# Phase 2: Expanding Macros

There are some distinct cases for a macro call which need to be handled carefully.

1) Text Argument
2) Single Element Argument
3) Mixed Element Argument


Text arguement, where the macro call has no child elements and only a
text element. The macro call has form: `<blue> arg </blue>`

```xml
<blue>
    this sentence is a text arguemnt 
</blue>
```

Element argument, where the macro call has a single child element

```xml
<blue> 
    <div>
        this div is an element argument
    </div> 
</blue>
```

The element may have tail text associated with it

```xml
<blue> 
    <div>
        this div is an element argument
    </div> 
    
    tail text
</blue>
```

Mixed argument, where the macro call element has a text node some
elements that may have tails.

```xml
<blue> 
    node text
    
    <div>
        this div is an element argument
    </div> 

    <div>
        this div is the second element
    </div> 

    node tail
</blue>
```


# Example 1) Text Argument.

```xml
<blue> this sentence is a text arguement </blue>
```

Suppose the macro associate with <blue> ... </blue> is

```xml
<define-macro name="blue"> <span class="blue-css-rule"> <contents/> </span> </define-macro>
```

The macro definition has a special key element called `<contents/>`
which is replaced by the contents of the macro call. In this example that is 

```
<blue> this sentence is a text argument </blue>
      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

So expanding the macro will result in:

```xml
<span class="blue-css-rule">  this sentence is a text argument  </span> 
                            !^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^!
```

Where the white space is preserved. Notice that the argument becomes
the text node of the `<span>` element, which is the parent of the
`<content/>` node of the macro definition.


