"""
Unsafe hash functions

Here we hash the user's input, but the vulnerability is simply using these
weak hash functions in the first place.
"""

import hashlib
from vulnpy.vendor import six


def _hash(hasher, user_input):
    b = six.ensure_binary(user_input, errors="ignore")
    hasher.update(b)
    return hasher.hexdigest()


def do_hashlib_md5(user_input):
    h = hashlib.md5()
    return _hash(h, user_input)


def do_hashlib_sha1(user_input):
    h = hashlib.sha1()
    return _hash(h, user_input)


def do_hashlib_new(user_input):
    h = hashlib.new("SHA256")
    return _hash(h, user_input)
