import os

import vulnpy

TEMPLATES_LOCATION = os.path.join(os.path.dirname(vulnpy.__file__), "templates")


def cache(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


@cache
def get_template(path):
    """
    Read and return the contents of the file at TEMPLATES_LOCATON/<path>.
    This is vulnerable to path traversal if used incorrectly, but security clearly
    isn't a concern if you're using `vulnpy`.
    """
    filename = os.path.join(TEMPLATES_LOCATION, path)
    with open(filename, "r") as f:
        return f.read()
