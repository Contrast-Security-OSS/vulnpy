from vulnpy.trigger import xpath
from tests.trigger.base_test import BaseTriggerTest


class TestLxmlEtreeFindall(BaseTriggerTest):
    @property
    def trigger_func(self):
        return xpath.do_lxml_etree_findall

    @property
    def good_input(self):
        return "./planet[name='Kepler']", "Kepler"

    @property
    def exception_input(self):
        return None


class TestLxmlEtreeFindText(BaseTriggerTest):
    @property
    def trigger_func(self):
        return xpath.do_lxml_etree_findtext

    @property
    def good_input(self):
        return ".//name", "Kepler"

    @property
    def exception_input(self):
        return None


class TestLxmlEtreeElementTreeFindall(BaseTriggerTest):
    @property
    def trigger_func(self):
        return xpath.do_xml_etree_elementtree_findall

    @property
    def good_input(self):
        return "./planet[name='Kepler']", "Kepler"

    @property
    def exception_input(self):
        return None
