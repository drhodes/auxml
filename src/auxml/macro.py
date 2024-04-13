from lxml import etree
from copy import deepcopy
from auxml.util import *

'''
<define-macro name="blue"><span style="color: #00f"><b><contents/></b></span></define-macro>
'''

'''
An element based macro call, it operates on <text>stuff</text>
<blue><text>stuff</text></blue> 
'''

def tail(el):
    if el.tail:
        return el.tail
    else:
        return ""

class MacroDef():
    def __init__(self, el):
        self.el = el
        self.name = el.get("name")

    def replace_one_var(self, el, varname, valuem):
        pass

    def ensure_names_match(self, mcall):
        assert mcall.name() == self.name

    def get_body(self):
        # the following line assumes the macro body only has one element.
        # TODO let macros definition have text and elements.
        return deepcopy(self.el.getchildren()[0])
    
    def expand_element_based(self, mcall):
        body = self.get_body()
        
        for content in body.findall(".//contents"):
            if mcall.has_children():
                inner = mcall.inner()
                content.getparent().replace(content, inner)
                return body
            else:
                raise Exception("need to handle text based macro call")
        raise Exception("dead code")
    
    def expand_text_based(self, mcall):
        body = self.get_body()
        for content in body.findall(".//contents"):
            par = content.getparent()
            par.remove(content)
            if par.text:
                par.text += mcall.text() + tail(content)
            else:
                par.text = mcall.text() + tail(content)
                
        return body
    
    def expand_mixed(self, mcall):
        body = self.get_body()
        for content in body.findall(".//contents"):
            par = content.getparent()            
            par.remove(content)
            if par.text:
                par.text += mcall.text()
            else: 
                par.text = mcall.text()
            for e in mcall.getchildren():
                par.append(deepcopy(e))
                
            if content.tail is None: continue            
            # append the tail of <content/> to the tail of the last element in par.
            
            last = par.getchildren()[-1]
            if last.tail == None:
                last.tail = content.tail
            else:
                last.tail += content.tail
        return body

    def expand_empty(self, mcall):
        return self.get_body()

    def replace_attrs(self, mcall, mac):
        s = etree.tostring(mac).decode("utf8")
        for av in self.attr_vars():
            tgt = f"[[{av}]]"
            val = mcall.get_attr(av)
            s = s.replace(tgt, val)
        tree = etree.fromstring(s)
        return tree

    def has_vars(self):
        return self.el.get("vars") is not None
    
    def attr_vars(self):
        if self.has_vars():
            return [x.strip() for x in self.el.get("vars").split(",")]
        return []
    
    def ensure_attrs_match(self, mcall):
        for var in self.attr_vars():
            if not mcall.contains_attr(var):
                raise Exception(f"Macro call on line ... must have attribute: {var}")
        
    def expand(self, mcall):
        self.ensure_names_match(mcall)
        self.ensure_attrs_match(mcall)
        
        mac = None
        if mcall.is_element_based():
            mac = self.expand_element_based(mcall)
        elif mcall.is_text_based():
            mac = self.expand_text_based(mcall)        
        elif mcall.is_mixed():
            mac = self.expand_mixed(mcall)
        elif mcall.is_empty(): 
            mac = self.expand_empty(mcall)           
        else:            
            raise Exception("Unhandled expansion, this is a bug")

        return self.replace_attrs(mcall, mac)
        
        
class MacroCall:    
    def __init__(self, el):
        self.el = el
        
    def name(self):
        return self.el.tag

    def text(self):
        return self.el.text

    def contains_attr(self, attr):
        return self.el.get(attr) is not None

    def get_attr(self, attr):
        return self.el.get(attr)
    
    def getchildren(self):
        return self.el.getchildren()
    
    def number_children(self):
        return len(self.getchildren())
    
    def has_children(self):
        return self.number_children() > 0
    
    def has_no_children(self):
        return not self.has_children()

    def has_one_child(self):
        return self.number_children() == 1

    def has_no_text(self):
        return self.el.text == None or self.el.text.strip() == ""

    def has_text(self):
        return not self.has_no_text()
    
    def is_element_based(self):
        return self.has_one_child() and self.has_no_text()

    def is_text_based(self):
        return self.has_no_children() and self.has_text()

    def is_mixed(self):
        return self.has_children() and self.has_text()

    def is_empty(self):
        return self.has_no_children() and self.has_no_text()
    
    def inner(self):
        if self.has_children():
            return deepcopy(self.el.getchildren()[0])
        else:
            raise Exception("")



