import os
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

        for macfile in cmdline.macro_files:
            mm.load_macro_file(macfile)

        fname = cmdline.infile
        root = parse_html_file(fname)
        
        expanded = mm.expand_all(fname, root)
        patched = self.patchup(expanded)
        self.save(patched)
        
    # todo move this patchup out to a python file specified by
    # cmdline args.
    def patchup_one(self, expanded, el):
    
        def patchup_sidebar(tree, el):
            el.tag = "div"
            # get all page elements
            pages = tree.xpath('//*[@class="page"]')
            for page in pages:
                url = f"/lectures/{page.get('path')}.html"
                new_el = etree.Element("a", attrib={"href": url })
                new_el.text = page.get("title")
                div = etree.Element("div")
                div.append(new_el)
                el.append(div)
            return tree
        
        functions = { "patchup_sidebar" : patchup_sidebar }

        func_name = el.get("func")
        if func_name is None:
            raise Exception("patchup element must have a `func` attribute that specifies patch function: todo import this err")

        if func_name not in functions:
            raise Exception(f"patchup function not found")
        
        return patchup_sidebar(expanded, el)
        
        

    def patchup(self, expanded):
        # stages
        # stage1 expansion
        # stage2 patch up

        els = expanded.xpath('//patchup')
        if len(els) == 0:
            print("warning: no outfile tags were found, therefore no outputs files were created")
        
        for el in els:
            self.patchup_one(expanded, el)        
        return expanded
    
    def save_one_outfile(self, el):
        relpath = el.get("path")
        
        if not relpath: raise Error("no relpath found: todo impve this err")
        
        fullpath = f'{cmdline.build_dir}/{relpath}'
        
        print("writing outfile: " + fullpath)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        
        with open(fullpath, 'wb') as f:
            text = "<!DOCTYPE html>".encode('utf-8')
            if el.text: text += el.text.encode('utf-8')
            children = el.getchildren()
            for c in children:
                text += etree.tostring(c, method="html")
            if el.tail:
                text += el.tail.encode('utf-8')
            f.write(text)
        
    def save_all_outfiles(self, node):
        # extract all the <outfile> tags
        # save their contents out to disk
        # !! todo: ensure outfile elements do not contain outfile elements. !!
        
        els = node.xpath('//outfile')
        if len(els) == 0:
            print("warning: no outfile tags were found, therefore no outputs files were created")
        
        for el in els:
            self.save_one_outfile(el)
        
    def save(self, el):
        remove_debug_attrs(el)
        self.save_all_outfiles(el)


def main():
    App()
    
