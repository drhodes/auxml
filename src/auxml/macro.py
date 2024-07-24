from lxml import etree
from copy import deepcopy
from auxml.util import *
from auxml.err import SyntaxErrorAuXML
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

def append_tail(el, s):
    if el.tail is None:
        el.tail = s
    else:
        el.tail += s
    
    
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
        cs = self.el.getchildren()
        
        if len(cs) == 0:
            raise SyntaxErrorAuXML(f"Encountered empty macro body in macro definition: `{self.name}`")
        
        if len(cs) > 1:
            msg = "macro definitions may not yet have more than one element"
            raise SyntaxErrorAuXML(msg)
        
        return deepcopy(self.el.getchildren()[0])
    
    def expand_empty(self, mcall):
        return self.get_body()

    def replace_attrs(self, mcall, mac):
        s = etree.tostring(mac).decode("utf8")
        for av in self.attr_vars():
            tgt = f"[[{av}]]"
            val = mcall.get_attr(av)
            s = s.replace(tgt, val)

        # the macro should have a unique identifier available to the macrocall
        s = s.replace("[[this]]", mcall.unique_id())
            
        # if `s` has a tail it won't parse so.. wrap it in a temporary
        # element tag, then extract it. Maybe there's a better way to
        # do this.
        
        try:
            tree = etree.fromstring("<temp>" + s + "</temp>")
            return tree.getchildren()[0]
        except Exception as e:
            print(s)
            raise e

    def has_vars(self):
        return self.el.get("vars") is not None
    
    def attr_vars(self):
        if self.has_vars():
            return [x.strip() for x in self.el.get("vars").split(",")]
        return []
    
    def ensure_attrs_match(self, mcall):
        for var in self.attr_vars():
            if not mcall.contains_attr(var):                
                raise Exception(f"Macro call: {mcall.name()} on line ... must have attribute: {var}")


    def replace_one_content(self, mcall, con):
        # identify calls cases.
        # <call> text </call>
        
        # identify <contents/> cases.
        # <tag> text <contents/> tail </tag>
        # <tag> text <contents/>      </tag>
        # <tag>      <contents/>      </tag>
        
        par = con.getparent()
        par.remove(con)
        if par.text is None:
            par.text = ""
        par.text += mcall.text() + tail(con)
            
    def expand_just_text(self, mcall):
        '''
        this is the case where mcall is replacing the <contents/>
        element with just a string.
        '''
        macrobody = self.get_body() # this is an element with no text or tail.
        for con in macrobody.findall(".//contents"):
            # mutating.
            prev = con.getprevious()
            if prev is not None:
                # CASE: <contents/> is being replaced by a string.
                # <tag> .. <tag> .. </tag> .. <contents/> <notail> </tag>
                # 
                append_tail(prev, mcall.text())
                con.getparent().remove(con)
            else:
                self.replace_one_content(mcall, con)
        return macrobody
            
    def expand_rest(self, mcall):        
        macrobody = self.get_body() # this is an element with no text or tail.
        # mcall will have at least one element.
        # mcall might have a tail, but callers will worry about that.

        # identify calls cases.
        # <call>      <el/>       </call>
        # <call> text <el/>       </call>
        # <call>      <el/> tail  </call>
        # <call> text <el/> tail  </call>        
        # <call> text <el1/> tail1 <el2/> tail2 </call>

        # identify <contents/> cases.
        # <tag> text <contents/> tail </tag>
        # <tag> text <contents/>      </tag>
        # <tag>      <contents/>      </tag>
       
        for con in macrobody.findall(".//contents"):
            par = con.getparent()
            idx = par.index(con)
            calltext = mcall.text()
            contail = tail(con)

            # handling the text node of the caller when replacing <contents/>
            if idx == 0:
                # <contents/> is the first element, so the callers
                # text nodes needs to be appended to the parents text
                # node, in other words splicing it in.
                if par.text is None: par.text = ""
                par.text += calltext
            else:
                # otherwise the <contents/> is somewhere in the middle
                # and has a previous element, therefore the callers
                # text node needs to be appended to the tail of the
                # previous element.
                prev = con.getprevious()
                if prev.tail is None: prev.tail = ""
                prev.tail += calltext
            
            for el in mcall.el.getchildren():
                idx += 1
                e = deepcopy(el)
                par.insert(idx, e)
        
            if len(par) > 0 and con.tail:
                if par[-1].tail is None:
                    par[-1].tail = ""
                par[-1].tail += contail
            par.remove(con)
        return macrobody
            
    def expand(self, mcall):
        self.ensure_names_match(mcall)
        self.ensure_attrs_match(mcall)
        
        if mcall.contains_attr("debug"):
            import pudb;pudb.set_trace()
        
        if mcall.is_empty(): 
            mac = self.expand_empty(mcall)
        elif mcall.is_just_text():
            mac = self.expand_just_text(mcall)
        else:
            mac = self.expand_rest(mcall)

        return self.replace_attrs(mcall, mac)
        
        
class MacroCall:
    counter = 0
    
    def __init__(self, el):
        self.el = el
        self.counter = MacroCall.counter
        MacroCall.counter += 1
        
    def unique_id(self):
        return f"{self.name()}-{self.counter}"
        
    def name(self):
        return self.el.tag

    def text(self):
        t = self.el.text
        return t if t else ""
    
    def contains_attr(self, attr):
        return self.el.get(attr) is not None

    def get_attr(self, attr):
        return self.el.get(attr)
    
    def getchildren(self):
        return self.el.getchildren()

    def is_just_text(self):
        return self.has_no_children() and self.has_text()
    
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
        return self.has_no_children() and self.has_text()

    def is_mixed(self):
        return self.has_children() and self.has_text()

    def is_empty(self):
        return self.has_no_children() and self.has_no_text()

    def show(self):
        return show(self.el)

    def __str__(self):
        return self.show()
