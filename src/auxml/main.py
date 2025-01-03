import argparse
import logging
import sys
from auxml.cmdline import cmdline
from auxml.macro_manager import MacroManager

from lxml import etree
from auxml.util import *
from auxml.parser import *
import auxml.directive as dt


class App():
    def __init__(self):
        mm = MacroManager()
        mm.register_directive("inline-html", dt.InlineHtml)
        
        mm.load_macro_file(cmdline.macros())

        fname = cmdline.infile()
        root = parse_html_file(fname)
        
        exp = mm.expand_all(fname, root)
        self.save(exp)

    def save(self, el):
        open(cmdline.outfile(), 'wb').write(etree.tostring(el, method="html"))
        
def main():
    App()
    
