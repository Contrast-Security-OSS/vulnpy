import io
import tarfile
import bz2


def do_tarfile_open(user_input):
    try:
        with tarfile.TarFile.open(user_input, mode="r:") as tf:
            return tf.getmembers()[0].name
    except Exception:
        return None


def do_tarfile_class(user_input):
    try:
        with tarfile.TarFile(user_input) as tf:
            return tf.getmembers()[0].name
    except Exception:
        return None


def do_tarfile_bz2(user_input):
    try:
        with tarfile.open(user_input, mode="r:bz2") as tf:
            return tf.getmembers()[0].name
    except Exception:
        return None


def do_bz2_class(user_input, size=0):
    try:
        with bz2.BZ2File(user_input) as bz2file:
            return bz2file.read(size)
    except Exception:
        return None


def do_bz2_open(user_input, size=0):
    try:
        with bz2.open(user_input) as bz2file:
            return bz2file.read(size)
    except Exception:
        return None


def do_io_open(user_input):
    try:
        with io.open(user_input) as f:
            return f.read()
    except Exception:
        return None


def do_open(user_input):
    """identical to io.open in PY3"""
    try:
        with open(user_input) as f:
            return f.read()
    except Exception:
        return None


def do_execfile(user_input):
    """only exists in PY2"""
    try:
        execfile(user_input)  # noqa: F821
    except Exception:
        pass
