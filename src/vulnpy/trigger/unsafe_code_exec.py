def do_exec(code):
    exec(code)


def do_eval(code):
    return eval(code)


def do_compile(code):
    return compile(code, "vulnpy.py", "exec")
