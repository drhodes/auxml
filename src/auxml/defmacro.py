from lxml import etree
from copy import deepcopy
from auxml.util import *

'''
<define-macro name="blue">
  <span style="color: #00f"><b><contents/></b></span>
</define-macro>
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

    def replace_content_tag(self):
        pass
    
    def expand(self, mcall):
        self.ensure_names_match(mcall)        
        newel = deepcopy(self.el)
        
        for content in newel.findall(".//contents"):
            if mcall.has_children():
                inner = mcall.inner()
                content.getparent().replace(content, inner)
            else:
                raise Exception("need to handle text based macro call")

            
class MacroCall:    
    def __init__(self, el):
        self.el = el
        
    def name(self):
        return self.el.tag
    
    def has_children(self):
        return len(self.el.getchildren()) > 0
    
    def inner(self):
        return deepcopy(self.el.getchildren()[0])



