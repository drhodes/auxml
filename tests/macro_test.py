import pudb
from lxml import etree
from xmldiff.diff import Differ
from auxml.macro import MacroDef, MacroCall
from auxml.macro_manager import MacroManager
from auxml.util import *

MacroDefBlue = '''<define-macro name="blue"><span style="color: #00f"><b><contents/></b></span></define-macro>'''
MacroCallBlue = '''<blue><text>stuff</text></blue>'''
BlueExpect = etree.fromstring('''<span style="color: #00f"><b><text>stuff</text></b></span>''')

def eq_trees(e1, e2):
    differ = Differ()
    diff = differ.diff(e1, e2)
    return len(list(diff)) == 0

def test_macro_def_blue():
    mac = MacroDef(etree.fromstring(MacroDefBlue))
    call = MacroCall(etree.fromstring(MacroCallBlue))
    el = mac.expand(call)
    assert eq_trees(el, BlueExpect)

def test_tree_diff1():
    s = "<div>asdf</div>"
    t = etree.fromstring(s)
    differ = Differ()
    diff = list(differ.diff(t,t))
    assert diff == []

def test_tree_diff2():
    t1 = etree.fromstring("<div>asdf</div>")
    t2 = etree.fromstring("<div>zxcv</div>")
    differ = Differ()
    diff = list(differ.diff(t1,t2))
    assert len(diff) > 0

def test_tree_diff3():
    t1 = etree.fromstring("<div>asdf</div>")
    t2 = etree.fromstring("<div>asdf </div>")
    differ = Differ()
    diff = list(differ.diff(t1,t2))
    assert len(diff) > 0

def equal_up_to_whitespace(e1, e2):
    differ = Differ()
    diff = list(differ.diff(e1, e2))
    for d in diff:
        ws1 = e1.xpath(d.node)[0].text.strip()
        ws2 = e2.xpath(d.node)[0].text.strip()
        if ws1 != ws2:
            return False
    return True
    
def test_up_to_whitespace1():
    t1 = etree.fromstring("<div>  asdf</div>")
    t2 = etree.fromstring("<div>asdf </div>")
    assert equal_up_to_whitespace(t1, t2)

def test_up_to_whitespace2():
    t1 = etree.fromstring("<div>  asdf      </div>")
    t2 = etree.fromstring("<div> asdf   </div>")
    assert equal_up_to_whitespace(t1, t2)

    
    
def test_macro_man():
    mm = MacroManager()
    mm.load_macro_file("./examples/macro-definitions/pb100-macros.xml")

def test_macro_man_expand():
    mm = MacroManager()
    mm.load_macro_file("./examples/macro-definitions/pb100-macros.xml")
    
