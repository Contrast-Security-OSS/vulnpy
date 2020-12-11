import re


def do_re_match(user_input):
    match = re.match(r"\(a*", user_input)
    if match:
        return match.group(0)


def do_re_search(user_input):
    match = re.search(r"\(a*", user_input)
    if match:
        return match.group(0)


def do_re_finditer(user_input):
    for match in re.finditer(r"\(a*", user_input):
        match.group(0)
