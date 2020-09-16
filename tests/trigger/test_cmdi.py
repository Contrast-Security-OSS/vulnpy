from vulnpy.trigger import cmdi
from tests.trigger.base_test import BaseTriggerTest


class TestOsSystem(BaseTriggerTest):
    @property
    def trigger_func(self):
        return cmdi.do_os_system

    @property
    def good_input(self):
        return "echo hacked", 0

    @property
    def exception_input(self):
        return None


class TestSubprocessPopen(BaseTriggerTest):
    @property
    def trigger_func(self):
        return cmdi.do_subprocess_popen

    @property
    def good_input(self):
        return "echo hacked", b"hacked\n"

    @property
    def exception_input(self):
        return None
