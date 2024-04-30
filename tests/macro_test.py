import sys
import pudb
from lxml import etree
from xmldiff.diff import Differ
from auxml.macro import MacroDef, MacroCall
from auxml.macro_manager import MacroManager
from auxml.util import *

MacroDefBlue = '''<define-macro name="blue"><span style="color: #00f"><b><contents/></b></span></define-macro>'''
MacroCallBlue = '''<blue><text>stuff</text></blue>'''
BlueExpect = etree.fromstring('''<span style="color: #00f"><b><text>stuff</text></b></span>''')

def cur_debugging():
    return hasattr(sys, 'gettrace') and sys.gettrace()

def eq_trees(got, exp):
    differ = Differ()
    diff = differ.diff(got, exp)
    is_same = len(list(diff)) == 0
    if not is_same:
        print("got:", show(got))
        print("exp:", show(exp))
        if cur_debugging(): import pudb;pudb.set_trace()
    return is_same

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

def with_mm(mac_strings, call_str, expect_str):
    call = etree.fromstring(call_str)
    exp  = etree.fromstring(expect_str)
    mm = MacroManager()
    
    for mac_str in mac_strings:
        mac  = etree.fromstring(mac_str)
        mm.add_macro_def(MacroDef(mac))
    got = mm.expand_all("nofile", call)
    assert eq_trees(got, exp)

def test_macro_def_green():
    m = '<define-macro name="green"><span style="color: #00f"><b><contents/></b></span></define-macro>'
    c = '<green> stuff <i>text</i> tail </green>'
    e = '<span style="color: #00f"><b> stuff <i>text</i> tail </b></span>'
    with_mm([m],c,e)

def test_macro_def_purple():
    m = '''<define-macro name="purple"><span style="color: #f0f"><b>AAA<contents/>BBB</b></span></define-macro>'''
    c = '''<purple> stuff <b>text</b> tail </purple>'''
    e = '''<span style="color: #f0f"><b>AAA stuff <b>text</b> tail BBB</b></span>'''
    with_mm([m],c,e)

def test_macro_def_A1():
    m = '<define-macro name="A1"><span><b>A<contents/>B</b><b>A<contents/>B</b></span></define-macro>'
    c = '<A1> stuff <b>text</b> tail </A1>'
    e = '<span><b>A stuff <b>text</b> tail B</b><b>A stuff <b>text</b> tail B</b></span>'
    with_mm([m],c,e)

def test_macro_empty():
    m = '<define-macro name="mac"><div></div></define-macro>'
    c = '<mac></mac>'
    e = '<div></div>' 
    with_mm([m],c,e)
    
def test_macro_empty2():
    m = '<define-macro name="mac"><div></div></define-macro>'
    c = '<mac/>'
    e = '<div></div>'
    with_mm([m],c,e)
    
def test_tail2():
    m = '<define-macro name="mac"><div><contents/></div></define-macro>'
    c = '<mac> rawr </mac>'
    e = '<div> rawr </div>'
    with_mm([m],c,e)
    
def test_tail3():
    m = '<define-macro name="mac"><div><contents/>B</div></define-macro>'
    c = '<mac>A</mac>'
    e = '<div>AB</div>'
    # import pudb;pudb.set_trace()
    with_mm([m],c,e)
   
def test_nested1():
    m = '<define-macro name="mac"><div><contents/></div></define-macro>'
    c = '<mac><mac>ASDF</mac></mac>'
    e = '<div><div>ASDF</div></div>' 
    with_mm([m],c,e)
    
def test_macro_empty_mm():
    m = '''<define-macro name="mac"><div></div></define-macro>'''
    c = '''<mac/>'''
    e = '''<div></div>'''
    with_mm([m], c, e)
    
def test_with_mm():
    m = '<define-macro name="mac"><div></div></define-macro>'
    c = '<mac/>'
    e = '<div></div>'
    with_mm([m], c, e)

def test_macro_def_text_based():
    m = '<define-macro name="text_based"><span style="color: #00f"><b> text <contents/> tail </b></span></define-macro>'
    c = '<text_based>stuff</text_based>'
    e = '<span style="color: #00f"><b> text stuff tail </b></span>'
    with_mm([m], c, e)
    
def test_mac_attrib1():
    m = '<define-macro name="square" vars="color, size"><div><div class="square"> is [[size]] meters wide and is the color [[color]]</div></div></define-macro>'
    c = '<square color="blue" size="30"/>'
    e = '<div><div class="square"> is 30 meters wide and is the color blue</div></div>'
    with_mm([m], c, e)

def test_mac_multi_call1():
    m1 = '<define-macro name="square"> <div class="square"></div></define-macro>'
    m2 = '<define-macro name="circle"> <div class="circle"></div></define-macro>'
    c = '<div><square/><circle/></div>'
    e = '<div><div class="square"></div><div class="circle"></div></div>'
    with_mm([m1, m2], c, e)
    
def test_mac_multi_call2():
    m1 = '<define-macro name="square"><div class="square">A</div></define-macro>'
    m2 = '<define-macro name="circle"><div class="circle"></div></define-macro>'
    c = '<div><square/><circle/></div>'
    e = '<div><div class="square">A</div><div class="circle"></div></div>'
    with_mm([m1, m2], c, e)
    
def test_mac_multi_call3():
    m1 = '<define-macro name="square"><div class="square">A</div></define-macro>'
    m2 = '<define-macro name="circle"><div class="circle">B</div></define-macro>'
    c = '<div><square/><circle/></div>'
    e = '<div><div class="square">A</div><div class="circle">B</div></div>'
    with_mm([m1, m2], c, e)

def test_mac_multi_call4():
    m1 = '<define-macro name="square"><div class="square">A</div></define-macro>'
    m2 = '<define-macro name="circle"><div class="circle">B</div></define-macro>'
    c = '<div>before<square/><circle/></div>'
    e = '<div>before<div class="square">A</div><div class="circle">B</div></div>'
    with_mm([m1, m2], c, e)

def test_mac_multi_call5():
    m1 = '<define-macro name="square"><div class="square">A</div></define-macro>'
    m2 = '<define-macro name="circle"><div class="circle">B</div></define-macro>'
    c = '<div><square/><circle/>after</div>'
    e = '<div><div class="square">A</div><div class="circle">B</div>after</div>'    
    with_mm([m1, m2], c, e)

def test_mac_multi_call6():
    m1 = '<define-macro name="square"><div class="square">A</div></define-macro>'
    c = '<div><square></square>after</div>'
    e = '<div><div class="square">A</div>after</div>'
    with_mm([m1], c, e)

def test_mac_multi_call7():
    m = '<define-macro name="m"><div>(<contents/>)</div></define-macro>'
    c = '<div><m><m>p</m><m>q</m></m></div>'
    e = '<div><div>(<div>(p)</div><div>(q)</div>)</div></div>'
    with_mm([m], c, e)

    
# this works.
def test_mac_multi_rearrange_bug2():
    m = '''
    <define-macro name="page" vars="title">
      <div><div>[[title]]</div>B</div>
    </define-macro>
    '''

    c = '<page title="A">B</page>'
    e = '''<div><div>A</div>B</div>'''
    with_mm([m], c, e)
    

def test_mac_multi_rearrange_bug():
    m = '''
    <define-macro name="page" vars="title">
      <div><div>[[title]]</div><contents/></div>
    </define-macro>
    '''

    c = '<page title="A">B</page>'
    e = '''<div><div>A</div>B</div>'''
    #pudb.set_trace()
    with_mm([m], c, e)
    

    
