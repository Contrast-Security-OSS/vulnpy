from vulnpy.trigger import redos


def test_re_fullmatch():
    redos.do_re_fullmatch("a")


def test_re_fullmatch_compiled():
    redos.do_re_fullmatch_compiled("a")
