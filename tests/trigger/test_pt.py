import os

import pytest
import six

from vulnpy.trigger import pt
from tests.trigger.base_test import BaseTriggerTest

SAMPLE_FILENAME = os.path.join(os.path.dirname(__file__), "samples", "sample.py")


class BaseOpenTest(BaseTriggerTest):
    @property
    def good_input(self):
        return SAMPLE_FILENAME, "a = 4 - 2\n"

    @property
    def exception_input(self):
        return "/definitely/not/a/file/"

    def test_exception(self):
        pass

    def test_exception_caught(self):
        assert self.trigger_func(self.exception_input) is None


class TestIoOpen(BaseOpenTest):
    @property
    def trigger_func(self):
        return pt.do_io_open


class TestOpen(BaseOpenTest):
    @property
    def trigger_func(self):
        return pt.do_open


@pytest.mark.skipif(six.PY2, reason="execfile only exists in PY2")
class TestExecfile(BaseOpenTest):
    @property
    def trigger_func(self):
        return pt.do_execfile

    @property
    def good_input(self):
        return SAMPLE_FILENAME, None
