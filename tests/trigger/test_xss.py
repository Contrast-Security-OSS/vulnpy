from vulnpy.trigger import xss
from tests.trigger.base_test import BaseTriggerTest


class TestRawXss(BaseTriggerTest):
    @property
    def trigger_func(self):
        return xss.do_raw

    @property
    def good_input(self):
        return "", ""

    def test_exception(self):
        import sys

        if sys.version_info[:2] == (3, 8):
            raise ValueError("Testing for CircleCI!")
