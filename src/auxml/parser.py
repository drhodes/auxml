from lxml import etree

_html_parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
_xml_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)

def parse_html_file(fname):
    tree = etree.parse(fname, _html_parser)
    return tree.getroot()
   
def parse_xml_file(fname):
    tree = etree.parse(fname, _xml_parser)
    return tree.getroot()

