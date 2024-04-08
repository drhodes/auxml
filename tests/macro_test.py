import pudb
from lxml import etree
from auxml.defmacro import MacroDef, MacroCall


MacroDefBlue = '''
<define-macro name="blue">
  <span style="color: #00f"><b><contents/></b></span>
</define-macro>
'''

MacroCallBlue = '''
<blue>
  <text>stuff</text>
</blue>
'''


def test_macro_def_blue():
    mac = MacroDef(etree.fromstring(MacroDefBlue))
    call = MacroCall(etree.fromstring(MacroCallBlue))
    mac.expand(call)
    pass
