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

    def get_body(self):
        # the following line assumes the macro body only has one element.
        # TODO let macros definition have text and elements.
        return deepcopy(self.el.getchildren()[0])
    
    def expand_element_based(self, mcall):
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
        body = self.get_body()
        for content in body.findall(".//contents"):
            par = content.getparent()
            # what if content has a tail?
            par.remove(content)
            par.text = mcall.text()
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
    
    def expand(self, mcall):
        self.ensure_names_match(mcall)
        
        if mcall.is_element_based():
            return self.expand_element_based(mcall)
        elif mcall.is_text_based():
            return self.expand_text_based(mcall)        
        elif mcall.is_mixed():
            return self.expand_mixed(mcall)
        elif mcall.is_empty(): 
            return self.expand_empty(mcall)
           
        else:            
            raise Exception("Unhandled expansion, this is a bug")

class MacroCall:    
    def __init__(self, el):
        self.el = el
        
    def name(self):
        return self.el.tag

    def text(self):
        return self.el.text

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



