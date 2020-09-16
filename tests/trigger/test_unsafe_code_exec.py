import mock

from vulnpy.trigger import unsafe_code_exec
from tests.trigger.base_test import BaseTriggerTest


class TestExec(BaseTriggerTest):
    @property
    def trigger_func(self):
        return unsafe_code_exec.do_exec

    @property
    def good_input(self):
        return 'print("foo")', None

    @property
    def exception_input(self):
        return None

    @mock.patch("sys.stdout.write")
    def test_good_input(self, mock_write):
        self.trigger_func(self.good_input[0])
        assert mock_write.called
        assert mock_write.call_args_list[0][0][0] == "foo"


class TestEval(BaseTriggerTest):
    @property
    def trigger_func(self):
        return unsafe_code_exec.do_eval

    @property
    def good_input(self):
        return "1 + 1", 2

    @property
    def exception_input(self):
        return '42 + "foo"'


class TestCompile(BaseTriggerTest):
    @property
    def trigger_func(self):
        return unsafe_code_exec.do_compile

    @property
    def good_input(self):
        return 'print("foo")', None

    @property
    def exception_input(self):
        return None

    @mock.patch("sys.stdout.write")
    def test_good_input(self, mock_write):
        code = self.trigger_func(self.good_input[0])
        exec(code)
        assert mock_write.called
        assert mock_write.call_args_list[0][0][0] == "foo"
