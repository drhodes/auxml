import sys
import re
from lxml import etree
from bs4 import BeautifulSoup
import pudb

_html_parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
_xml_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

ATTR_FILENAME = 'auxml-data-filename'
ATTR_LINENUM = 'auxml-data-line'

def el_location_info(el):
    filename = el.get(ATTR_FILENAME)
    linenum = el.get(ATTR_LINENUM)
    return f'''
    in file   ...... : {filename}
    on line number.. : {linenum}
    '''

def tag_els_with_info(el, fname):
    if hasattr(el, 'sourceline'): 
        line_number = el.sourceline
        el[ATTR_FILENAME] = fname
        el[ATTR_LINENUM] = str(line_number)
    
    for child in el.children:
        if isinstance(child, str):
            continue        
        tag_els_with_info(child, fname)

def parse_html_file(fname):
    text = open(fname).read()
    soup = BeautifulSoup(text, "html.parser")
    
    # mutate soup in place
    tag_els_with_info(soup, fname)

    escaped_html = str(soup)
    try:
        tree = etree.fromstring(escaped_html, _xml_parser)
        return tree
    except etree.XMLSyntaxError as e:
        error_message = str(e)
        match = re.search(r'line (\d+), column (\d+)', error_message)
        if match:
            line, column = map(int, match.groups())
            hint1 = open(fname).readlines()[line-1].strip()
            hint2 = (column-1) * '·' + "^"
        else:
            line, column, hint = None, None, None
        msg = f'''
        Had trouble parsing some HTML
          filename : {fname}
          on line  : {line}
          column   : {column}
          
{hint1}
{hint2}
        
        '''
        if line and column:
            raise SyntaxError(msg)
        else:
            raise
            
def parse_string(s):
    soup = BeautifulSoup(s, "html.parser")
    tree = etree.fromstring(str(soup), _xml_parser)
    return tree

# mutates
def deep_rm_attr(el, attr_name):    
    '''recursively descend through all elements removing attributes
    with `attr_name`.'''
    
    if el is None:
        return
    
    if attr_name in el.attrib:
        del el.attrib[attr_name]
        
    for child in el:
        deep_rm_attr(child, attr_name)


# mutates
def remove_debug_attrs(el):
    deep_rm_attr(el, ATTR_FILENAME)
    deep_rm_attr(el, ATTR_LINENUM)
