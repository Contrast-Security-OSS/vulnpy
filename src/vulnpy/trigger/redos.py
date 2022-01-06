import re

PATTERN = r"((a)+)+"


def do_re_match(user_input):
    match = re.match(PATTERN, user_input)
    if match:
        return match.group(0)


def do_re_match_compiled(user_input):
    pattern = re.compile(PATTERN)
    match = pattern.match(user_input)
    if match:
        return match.group(0)


def do_re_search(user_input):
    match = re.search(PATTERN, user_input)
    if match:
        return match.group(0)


def do_re_search_compiled(user_input):
    pattern = re.compile(PATTERN)
    match = pattern.search(user_input)
    if match:
        return match.group(0)


def do_re_finditer(user_input):
    for match in re.finditer(PATTERN, user_input):
        match.group(0)


def do_re_finditer_compiled(user_input):
    pattern = re.compile(PATTERN)
    for match in pattern.finditer(user_input):
        match.group(0)


def do_re_findall(user_input):
    return re.findall(PATTERN, user_input)


def do_re_findall_compiled(user_input):
    pattern = re.compile(PATTERN)
    return pattern.findall(user_input)


def do_re_fullmatch(user_input):
    match = re.fullmatch(PATTERN, user_input)
    if match:
        return match.group(0)


def do_re_fullmatch_compiled(user_input):
    pattern = re.compile(PATTERN)
    match = pattern.fullmatch(user_input)
    if match:
        return match.group(0)


def do_re_sub(user_input):
    return re.sub(PATTERN, "anything", user_input)


def do_re_sub_compiled(user_input):
    pattern = re.compile(PATTERN)
    return pattern.sub("anything", user_input)


def do_re_subn(user_input):
    return re.subn(PATTERN, "anything", user_input)


def do_re_subn_compiled(user_input):
    pattern = re.compile(PATTERN)
    return pattern.subn("anything", user_input)


def do_re_split(user_input):
    return re.split(PATTERN, user_input)


def do_re_split_compiled(user_input):
    pattern = re.compile(PATTERN)
    return pattern.split(user_input)
