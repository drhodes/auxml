import pytest
import sys
import pudb
from lxml import etree
from xmldiff.diff import Differ
from auxml.macro import MacroDef, MacroCall
from auxml.macro_manager import MacroManager
from auxml.util import *
from auxml.err import SyntaxErrorAuXML


def with_mm_file(filename):
    mm = MacroManager()
    mm.load_macro_file(filename)
        
def test_fileinfo():
    with_mm_file("tests/test-html/macros-multiargs.html")

