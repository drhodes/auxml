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
    s = "<div>div</div>"
    t = etree.fromstring(s)
    differ = Differ()
    diff = list(differ.diff(t,t))
    assert diff == []

def test_tree_diff2():
    t1 = etree.fromstring("<div>div</div>")
    t2 = etree.fromstring("<div>zxcv</div>")
    differ = Differ()
    diff = list(differ.diff(t1,t2))
    assert len(diff) > 0

def test_tree_diff3():
    t1 = etree.fromstring("<div>div</div>")
    t2 = etree.fromstring("<div>div </div>")
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
    t1 = etree.fromstring("<div>  div</div>")
    t2 = etree.fromstring("<div>div </div>")
    assert equal_up_to_whitespace(t1, t2)

def test_up_to_whitespace2():
    t1 = etree.fromstring("<div>  div      </div>")
    t2 = etree.fromstring("<div> div   </div>")
    assert equal_up_to_whitespace(t1, t2)

    
    
def test_macro_man():
    mm = MacroManager()
    mm.load_macro_file("./examples/macro-definitions/pb100-macros.xml")

def test_macro_man_expand():
    mm = MacroManager()
    mm.load_macro_file("./examples/macro-definitions/pb100-macros.xml")
    

 
MacroDefText_Based = '''<define-macro name="text_based"><span style="color: #00f"><b> text <contents/> tail </b></span></define-macro>'''
MacroCallText_Based = '''<text_based>stuff</text_based>'''
Text_BasedExpect = etree.fromstring('''<span style="color: #00f"><b> text stuff tail </b></span>''')

def test_macro_def_text_based():
    mac = MacroDef(etree.fromstring(MacroDefText_Based))
    call = MacroCall(etree.fromstring(MacroCallText_Based))
    el = mac.expand(call)
    # import pudb;pudb.set_trace()
    assert eq_trees(el, Text_BasedExpect)


MacroDefGreen = '''<define-macro name="green"><span style="color: #00f"><b><contents/></b></span></define-macro>'''
MacroCallGreen = '''<green> stuff <inner>text</inner> tail </green>'''
GreenExpect = etree.fromstring('''<span style="color: #00f"><b> stuff <inner>text</inner> tail </b></span>''')

def test_macro_def_green():
    mac = MacroDef(etree.fromstring(MacroDefGreen))
    call = MacroCall(etree.fromstring(MacroCallGreen))
    el = mac.expand(call)
    #import pudb;pudb.set_trace()
    assert eq_trees(el, GreenExpect)



MacroDefPurple = '''<define-macro name="purple"><span style="color: #f0f"><b>AAA<contents/>BBB</b></span></define-macro>'''
MacroCallPurple = '''<purple> stuff <inner>text</inner> tail </purple>'''
PurpleExpect = etree.fromstring('''<span style="color: #f0f"><b>AAA stuff <inner>text</inner> tail BBB</b></span>''')

def test_macro_def_purple():
    mac = MacroDef(etree.fromstring(MacroDefPurple))
    call = MacroCall(etree.fromstring(MacroCallPurple))
    el = mac.expand(call)
    # import pudb;pudb.set_trace()
    assert eq_trees(el, PurpleExpect)
    


MacroDefA1 = '''<define-macro name="A1"><span><b>A<contents/>B</b><b>A<contents/>B</b></span></define-macro>'''
MacroCallA1 = '''<A1> stuff <inner>text</inner> tail </A1>'''
A1Expect = etree.fromstring('''<span><b>A stuff <inner>text</inner> tail B</b><b>A stuff <inner>text</inner> tail B</b></span>''')

def test_macro_def_A1():
    mac = MacroDef(etree.fromstring(MacroDefA1))
    call = MacroCall(etree.fromstring(MacroCallA1))
    el = mac.expand(call)
    # import pudb;pudb.set_trace()
    assert eq_trees(el, A1Expect)
    

def test_macro_empty():
    mdef = '''<define-macro name="mac"><div></div></define-macro>'''
    mcall = '''<mac></mac>'''
    exp = etree.fromstring('''<div></div>''')
    
    mac = MacroDef(etree.fromstring(mdef))
    call = MacroCall(etree.fromstring(mcall))
    el = mac.expand(call)
    assert eq_trees(el, exp)
    
    
def test_macro_empty2():
    mdef = '''<define-macro name="mac"><div></div></define-macro>'''
    mcall = '''<mac/>'''
    exp = etree.fromstring('''<div></div>''')
    
    mac = MacroDef(etree.fromstring(mdef))
    call = MacroCall(etree.fromstring(mcall))
    el = mac.expand(call)
    assert eq_trees(el, exp)
    
    
def test_tail2():
    mdef = '''<define-macro name="mac"><div><contents/></div></define-macro>'''
    mcall = '''<mac> div </mac>'''
    exp = etree.fromstring('''<div> div </div>''')
    
    mac = MacroDef(etree.fromstring(mdef))
    call = MacroCall(etree.fromstring(mcall))
    el = mac.expand(call)
    assert eq_trees(el, exp)
    
    
def test_tail3():
    mdef = '''<define-macro name="mac"><div><contents/> div </div></define-macro>'''
    mcall = '''<mac> div </mac>'''
    exp = etree.fromstring('''<div> div  div </div>''')
    
    mac = MacroDef(etree.fromstring(mdef))
    call = MacroCall(etree.fromstring(mcall))
    el = mac.expand(call)
    assert eq_trees(el, exp)

   
def test_nested1():
    mdef = '''<define-macro name="mac"><div><contents/></div></define-macro>'''
    mcall = '''<mac><mac>ASDF</mac></mac>'''
    exp = etree.fromstring('''<div><div>ASDF</div></div>''')
    
    mac = MacroDef(etree.fromstring(mdef))
    mm = MacroManager()
    mm.add_macro_def(mac)
    
    call = etree.fromstring(mcall)
    el = mm.expand_all(call)
    assert eq_trees(el, exp)
    
    
def test_macro_empty_mm():
    mac  = etree.fromstring('''<define-macro name="mac"><div></div></define-macro>''')
    call = etree.fromstring('''<mac/>''')
    exp  = etree.fromstring('''<div></div>''')
    
    mm = MacroManager()
    mm.add_macro_def(MacroDef(mac))
    el = mm.expand_all(call)
    assert eq_trees(el, exp)


def with_mm(mac_str, call_str, expect_str):
    mac  = etree.fromstring(mac_str)
    call = etree.fromstring(call_str)
    exp  = etree.fromstring(expect_str)
    mm = MacroManager()
    mm.add_macro_def(MacroDef(mac))
    el = mm.expand_all(call)
    assert eq_trees(el, exp)
    
    
def test_with_mm():
    m = '<define-macro name="mac"><div></div></define-macro>'
    c = '<mac/>'
    e = '<div></div>'
    with_mm(m, c, e)
    
# def test_mac_attrib1():
#     m = '<define-macro name="square" vars="color, size"><div><div class="square"> is [[size]] meters wide and is the color [[color]]</div></div></define-macro>'
#     c = '<mac/>'
#     e = '<div></div>'
#     with_mm(m, c, e)
    
