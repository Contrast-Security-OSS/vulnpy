import os

from vulnpy.trigger import pt
from tests.trigger.base_test import BaseTriggerTest

SAMPLE_FILENAME = os.path.join(os.path.dirname(__file__), "samples", "sample.py")
SAMPLE_TARFILE = os.path.join(os.path.dirname(__file__), "samples", "sample.tar")
SAMPLE_BZ2_FILE = os.path.join(os.path.dirname(__file__), "samples", "sample.tar.bz2")


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


class TestTarfileOpen(BaseOpenTest):
    @property
    def good_input(self):
        return SAMPLE_TARFILE, "test"

    @property
    def trigger_func(self):
        return pt.do_tarfile_open


class TestTarfileOpenClass(BaseOpenTest):
    @property
    def good_input(self):
        return SAMPLE_TARFILE, "test"

    @property
    def trigger_func(self):
        return pt.do_tarfile_class


class TestTarfileBZ2Open(BaseOpenTest):
    @property
    def good_input(self):
        return SAMPLE_BZ2_FILE, "test"

    @property
    def trigger_func(self):
        return pt.do_tarfile_bz2


class TestBZ2Open(BaseOpenTest):
    @property
    def good_input(self):
        return SAMPLE_BZ2_FILE, b"test"

    def test_good_input(self):
        assert self.trigger_func(self.good_input[0], 4) == self.good_input[1]

    @property
    def trigger_func(self):
        return pt.do_bz2_open


class TestBZ2OpenClass(BaseOpenTest):
    @property
    def good_input(self):
        return SAMPLE_BZ2_FILE, b"test"

    def test_good_input(self):
        assert self.trigger_func(self.good_input[0], 4) == self.good_input[1]

    @property
    def trigger_func(self):
        return pt.do_bz2_class


class TestOpen(BaseOpenTest):
    @property
    def trigger_func(self):
        return pt.do_open


class TestExecfile(BaseOpenTest):
    @property
    def trigger_func(self):
        return pt.do_execfile

    @property
    def good_input(self):
        return SAMPLE_FILENAME, None
