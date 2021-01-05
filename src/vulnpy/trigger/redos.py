import re
from vulnpy.vendor import six


def do_re_match(user_input):
    match = re.match(r"((a)+)+", user_input)
    if match:
        return match.group(0)


def do_re_search(user_input):
    match = re.search(r"((a)+)+", user_input)
    if match:
        return match.group(0)


def do_re_finditer(user_input):
    for match in re.finditer(r"((a)+)+", user_input):
        match.group(0)


def do_re_findall(user_input):
    return re.findall(r"((a)+)+", user_input)


def do_re_fullmatch(user_input):
    if six.PY2:
        # fulmmatch is Py3 only
        return None

    match = re.fullmatch(r"((a)+)+", user_input)
    if match:
        return match.group(0)


def do_re_sub(user_input):
    return re.sub(r"((a)+)+", "anything", user_input)


def do_re_subn(user_input):
    return re.subn(r"((a)+)+", "anything", user_input)


def do_re_split(user_input):
    return re.split(r"((a)+)+", user_input)
