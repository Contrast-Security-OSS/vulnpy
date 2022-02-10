import lxml.etree
import xml.etree.ElementTree as ET
from io import StringIO

xml = """
    <planets>
        <planet>
            <name>Kepler</name>
        </planet>
        <planet>
            <name>Mars</name>
        </planet>
        <planet>
            <name>Newton</name>
        </planet>
    </planets>
"""

tree = lxml.etree.parse(StringIO(xml))
tree.xpath('/planet[name[text()="Kepler"]]')
root = tree.getroot()


def do_lxml_etree_findall(user_input):
    return root.findall(user_input)[0][0].text


def do_lxml_etree_findtext(user_input):
    return root.findtext(user_input)


def do_xml_etree_elementtree_findall(user_input):
    node = ET.fromstring(xml)
    return node.findall(user_input)[0][0].text
