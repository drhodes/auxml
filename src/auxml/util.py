from lxml import etree

def all_element_text(el):
    text = ""
    text += el.text if el.text else  ""
    for e in el.getchildren():
        text += all_element_text(e)
    text = text.replace("[mathjaxinline]", "")
    text = text.replace("[/mathjaxinline]", "")
    return text.strip()
    
def new_div(classname):
    div = etree.Element("div")
    div.set("class", classname)
    return div

def new_span(classname):
    span = etree.Element("span")
    span.set("class", classname)
    return span

def copy_attribs(src, tgt):
    for key, val in src.attrib.items():
        tgt.set(key, val)

def div_from(obj):
    div = new_div(obj.el.tag)
    copy_attribs(obj.el, div)
    return div

def in_div(el):
    div = etree.Element("div")
    div.append(el)
    return div

def clone_element_without_elements(el):
    newel = etree.Element(el.tag)
    copy_attribs(el, newel)
    newel.text = el.text
    newel.tail = el.tail
    return newel

def title_wrap(div, obj, name):
    title = new_div(f"{name}-title")
    wrapper = new_div(f"{name}-wrapper")
    title.text = obj.display_name() 
    wrapper.append(title)
    wrapper.append(div)
    return wrapper

def add_class(el, css_classname):
    cur_classes = el.get("class", "")        
    el.set("class", f"{cur_classes} {css_classname}")
    return el

def showel(el):
    print(etree.tostring(el, pretty_print=True).decode())

def show(el):
    return etree.tostring(el, pretty_print=True).decode()
    
