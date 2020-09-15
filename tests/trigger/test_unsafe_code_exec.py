import mock
import pytest

from vulnpy.trigger import unsafe_code_exec


@mock.patch("sys.stdout.write")
def test_do_exec(mock_write):
    unsafe_code_exec.do_exec('print("foo")')
    assert mock_write.called
    assert mock_write.call_args_list[0][0][0] == "foo"


def test_do_eval():
    assert unsafe_code_exec.do_eval("37 + 5") == 42


def test_do_eval_exeception():
    with pytest.raises(TypeError):
        unsafe_code_exec.do_eval('42 + "foo"')


@mock.patch("sys.stdout.write")
def test_do_compile(mock_write):
    code = unsafe_code_exec.do_compile('print("foo")')

    exec(code)

    assert mock_write.called
    assert mock_write.call_args_list[0][0][0] == "foo"
