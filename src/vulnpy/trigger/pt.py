import io


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
        execfile(user_input)
    except Exception:
        pass
