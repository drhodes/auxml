import logging
from auxml.cmdline import cmdline
from lxml import etree
from auxml.parser import *



class InlineHtml():
    def __init__(self, el):
        self.el = el
    
    def run(self):
        fname = self.el.get("filename")
        
        if fname is None:
            raise Exception("the inline-html element must have attribute: `filename`")
            
        
        root = parse_html_file(fname)
        return root
