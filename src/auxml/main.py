import argparse
import logging
import sys
from auxml.cmdline import cmdline
from auxml.macro_manager import MacroManager


from lxml import etree
from auxml.util import *

class App():
    def __init__(self):
        mm = MacroManager()
        mm.load_macro_file(cmdline.macros())
        
        tree = etree.parse(cmdline.infile())
        root = tree.getroot()
        exp = mm.expand_all(root)
        self.save(exp)

    def save(self, el):
        outfile = f"{cmdline.build_dir()}/output.html"
        open(outfile, 'wb').write(etree.tostring(el, method="html"))
        
        
def main():
    App()
    
