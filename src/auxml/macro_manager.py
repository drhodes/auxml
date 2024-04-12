from lxml import etree 

from auxml.macro import MacroDef, MacroCall


class MacroManager():
    def __init__(self):
        self.macro_defs = {}
            
    def load_macro_file(self, infile):
        macros = etree.parse(infile)
        for el in macros.findall(".//define-macro"):
            macdef = MacroDef(el)
            self.add_macro_def(macdef)

    def add_macro_def(self, macdef):        
        if macdef.name in self.macro_defs:
            raise Exception(f"macro already defined: {macdef.name}")
        self.macro_defs[macdef.name] = macdef

    def expand_all(self, el):
        for e in el.getchildren():
            if e.tag in self.macro_defs:
                mac = self.macro_defs[e.tag]
                call = MacroCall(e)
                exp = self.expand_all(mac.expand(call))
                el.replace(e, exp)
                
        return el
