from lxml import etree
from bs4 import BeautifulSoup
_html_parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
_xml_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

def parse_html_file(fname):
    text = open(fname).read()
    soup = BeautifulSoup(text, "html.parser")
    tree = etree.fromstring(str(soup), _xml_parser)
    return tree
   
# def parse_xml_file(fname):
#     tree = etree.parse(fname, _xml_parser)
#     return tree.getroot()

