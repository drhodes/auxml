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

class MacroDef():
    def __init__(self, el):
        self.el = el
        self.name = el.get("name")

    def replace_one_var(self, el, varname, valuem):
        pass

    def ensure_names_match(self, mcall):
        assert mcall.name() == self.name
        
    def expand_element_based(self, mcall):
        self.ensure_names_match(mcall)        
        newel = deepcopy(self.el.getchildren()[0])
        
        for content in newel.findall(".//contents"):
            if mcall.has_children():
                inner = mcall.inner()
                content.getparent().replace(content, inner)
                return newel
            else:
                raise Exception("need to handle text based macro call")
        raise Exception("dead code")

    def expand_text_based(self, mcall):
        pass
    
    def expand(self, mcall):
        if mcall.is_element_based():
            return self.expand_element_based(mcall)        
        

class MacroCall:    
    def __init__(self, el):
        self.el = el
        
    def name(self):
        return self.el.tag

    def number_children(self):
        return len(self.el.getchildren())
    
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
        return self.has_no_children() and self.has_text();
    
    def inner(self):
        if self.has_children():
            return deepcopy(self.el.getchildren()[0])
        else:
            raise Exception("")



