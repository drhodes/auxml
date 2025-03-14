from lxml import etree 
from copy import deepcopy

from auxml.macro import MacroDef, MacroCall
from auxml.util import *
from auxml.html_tags import is_an_html_tag
from auxml.parser import parse_html_file

from auxml.err import SyntaxErrorAuXML

class MacroManager():    
    """
    Manages macro definitions and directives for processing structured markup.

    This class allows registering directives, loading and expanding macros,
    and handling macro-based transformations within an HTML-like structure.
    """
   
    def __init__(self):
        self.macro_defs = {} # {tag : {args : macrodef}}
        self.directives = {}

    def register_directive(self, name, cls):
        self.directives[name] = cls
        
    def load_macro_file(self, infile):
        macros = parse_html_file(infile)
        for el in macros.findall(".//define-macro"):
            md = MacroDef(el)
            self.add_macro_def(md)

    def lookup(self, name, attr_vars):
        if name not in self.macro_defs:
            return None
        if attr_vars not in self.macro_defs[name]:
            return None        
        return self.macro_defs[name][attr_vars]

    def lookup_with_macdef(self, macdef):
        return self.lookup(macdef.name, macdef.attr_vars())

    def lookup_with_call(self, call):
        return self.lookup(call.name(), call.vars())
    
    def check_already_defined(self, macdef):
        # if macdef.name == "multi":
        #     import pudb;pudb.set_trace()
        if self.lookup_with_macdef(macdef) is not None:
            raise Exception(f"macro already defined: {macdef.name}")

    def insert(self, macdef):
        if macdef.name not in self.macro_defs:
            self.macro_defs[macdef.name] = {}
        self.macro_defs[macdef.name][macdef.attr_vars()] = macdef
        
    def add_macro_def(self, macdef):
        if is_an_html_tag(macdef.name):
            raise Exception(f"macro: `{macdef.name}` can't have the same name as an HTML tag")

        self.check_already_defined(macdef)
        
        if len(macdef.el.getchildren()) > 1:
            msg = f"macro `{macdef.name}` may not have more than one child element\n"
            msg += f"Got `{macdef.el.getchildren()}` child elements\n"
            raise SyntaxErrorAuXML(msg)
        #
        self.insert(macdef)
        # self.macro_defs[macdef.name] = macdef

    def valid_tag(self, el):
        tag = el.tag
        
        assert type(tag) == str        
        if tag == "contents":
            return True
        
        cond1 = tag in self.macro_defs
        cond2 = is_an_html_tag(tag)
        
        return (cond1 or cond2)

    def is_directive(self, tag):
        return tag == "inline-html"

    def run_directive(self, fname, el):
        if el.tag not in self.directives:
            raise Exception(f"tried to run directive: {el.tag}, however it does not exist")
        d = self.directives[el.tag](el)
        return self.expand_all(fname, d.run())
        
    
    def expand_all(self, fname, el):
        if self.is_directive(el.tag):
            result = self.run_directive(fname, el)
            return result
        
        if not self.valid_tag(el):
            raise Exception(f"In file: {fname}, on line: {el.sourceline}, found unknown tag: {el.tag}")
        
        if el.tag in self.macro_defs:
            # lookup !!
            call = MacroCall(el)
            mac = self.lookup_with_call(call)
            if mac is None:
                raise Exception(f"macro not found: {call.name} with vars {call.vars()}")

            tail = el.tail
            el = mac.expand(call)
            el.tail = tail
            
        for e in el.getchildren():
            exp = self.expand_all(fname, e)            
            el.replace(e, exp)

        if el.tag in self.macro_defs:
            return self.expand_all(fname, el)
        else:
            return el

    def __repr__(self):
        return f"<<MacroManager: {len(self.macro_defs)} registered macros>>"
