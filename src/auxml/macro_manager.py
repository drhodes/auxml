from lxml import etree 
from copy import deepcopy

from auxml.macro import MacroDef, MacroCall
from auxml.util import *
from auxml.html_tags import is_an_html_tag

class MacroManager():
    def __init__(self):
        self.macro_defs = {}
            
    def load_macro_file(self, infile):
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        # xml_root = etree.fromstring(xml, parser)
        macros = etree.parse(infile, parser)
        for el in macros.findall(".//define-macro"):
            macdef = MacroDef(el)
            self.add_macro_def(macdef)

    def add_macro_def(self, macdef):
        if is_an_html_tag(macdef.name):
            raise Exception(f"macro can't have the same name as an HTML tag")
        if macdef.name in self.macro_defs:
            raise Exception(f"macro already defined: {macdef.name}")
        self.macro_defs[macdef.name] = macdef

    def cant_find(self, tag):
        return not ((tag in self.macro_defs) or is_an_html_tag(tag))

    def expand_all(self, el):
        if el.tag in self.macro_defs:
            mac = self.macro_defs[el.tag]
            call = MacroCall(el)
            tail = el.tail
            el = mac.expand(call)
            el.tail = tail
            
        for e in el.getchildren():
            exp = self.expand_all(e)            
            el.replace(e, exp)

        if self.cant_find(el.tag):
            raise Exception(f"Can't seem to find tag: {el.tag} anywhere")
        return el

    def __repr__(self):
        return f"<<MacroManager: {len(self.macro_defs)} registered macros>>"
