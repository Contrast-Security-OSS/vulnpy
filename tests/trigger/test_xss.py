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
        pass
