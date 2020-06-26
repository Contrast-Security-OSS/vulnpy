import pytest

from vulnpy.trigger import cmdi


def test_do_os_system():
    assert cmdi.do_os_system("echo hacked") == 0


def test_do_os_system_bad_command():
    assert cmdi.do_os_system("barrrrrr bad command") != 0


def test_do_os_system_exception():
    with pytest.raises(TypeError):
        cmdi.do_os_system(None)


def test_do_subprocess_popen():
    assert cmdi.do_subprocess_popen(["echo", "hacked"]) == b"hacked\n"


def test_do_subprocess_popen_bad_command():
    with pytest.raises(OSError):
        cmdi.do_subprocess_popen(["foooooooo", "this", "is", "not", "a", "command"])


def test_do_subprocess_popen_exception():
    with pytest.raises(TypeError):
        cmdi.do_subprocess_popen(None)
