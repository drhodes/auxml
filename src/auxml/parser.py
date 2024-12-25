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
    tree = etree.fromstring(escaped_html, _xml_parser)
    return tree

def parse_string(s):
    soup = BeautifulSoup(s, "html.parser")
    tree = etree.fromstring(str(soup), _xml_parser)
    return tree
