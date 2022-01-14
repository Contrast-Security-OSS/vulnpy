"""
In PY3, urllib2 was ported mostly to urllib.request.
The original PY2 urllib module is unique to PY2.

In this module, we use urllib2 and urllib.request methods
interchangeably depending on the version of python. We refer
to the original PY2 urllib module as "legacy".
"""

import io
import mock
import os

from urllib.request import Request, urlopen
from http.client import HTTPConnection, HTTPSConnection

legacy_urlopen = urlopen


EXCEPTION_CODE = -100
TRUSTED_HOST = "example.com"
TRUSTED_METHOD = "GET"
TRUSTED_URL = "/"


def mock_connection(func):
    """
    Mock out socket connections for SSRF unless we see the
    VULNPY_REAL_SSRF_REQUESTS environment variable. This should
    only be used when vulnpy is being stood up as a real webapp.

    For unit testing with vulnpy, it's probably best to use the
    default behavior to avoid overloading some third-party server.
    """

    def wrapper(*args):
        if os.environ.get("VULNPY_REAL_SSRF_REQUESTS"):
            return func(*args)

        mock_socket = mock.MagicMock()
        mock_socket.makefile.return_value = io.BytesIO(b"HTTP/1.1 200 OK")
        with mock.patch("socket.create_connection", return_value=mock_socket):
            return func(*args)

    return wrapper


@mock_connection
def _urlopen(urlopen_func, arg):
    try:
        return urlopen_func(arg).getcode()
    except Exception:
        return EXCEPTION_CODE


def do_legacy_urlopen(user_input):
    """
    PY2: urllib.urlopen
    PY3: urllib.request.urlopen (fallback only, not intended for use)
    """
    return _urlopen(legacy_urlopen, user_input)


def do_urlopen_str(user_input):
    """
    PY2: urllib2.urlopen
    PY3: urllib.request.urlopen
    """
    return _urlopen(urlopen, user_input)


def do_urlopen_obj(user_input):
    """
    Same as urlopen_str, but first creates a request object.
    """
    try:
        req = Request(user_input)
    except Exception:
        req = None
    return _urlopen(urlopen, req)


@mock_connection
def _request(user_input, connection_class, method_name, vulnerable_url):
    try:
        c = connection_class(TRUSTED_HOST)

        request_method = getattr(c, method_name)
        if vulnerable_url:
            request_method(TRUSTED_METHOD, user_input)
        else:
            request_method(user_input, TRUSTED_URL)
        if method_name == "putrequest":
            c.endheaders()

        return c.getresponse().status
    except Exception:
        return EXCEPTION_CODE


def do_httpconnection_request_url(user_input):
    return _request(user_input, HTTPConnection, "request", True)


def do_httpconnection_request_method(user_input):
    return _request(user_input, HTTPConnection, "request", False)


def do_httpconnection_putrequest_url(user_input):
    return _request(user_input, HTTPConnection, "putrequest", True)


def do_httpconnection_putrequest_method(user_input):
    return _request(user_input, HTTPConnection, "putrequest", False)


def do_httpsconnection_request_url(user_input):
    return _request(user_input, HTTPSConnection, "request", True)


def do_httpsconnection_request_method(user_input):
    return _request(user_input, HTTPSConnection, "request", False)


def do_httpsconnection_putrequest_url(user_input):
    return _request(user_input, HTTPSConnection, "putrequest", True)


def do_httpsconnection_putrequest_method(user_input):
    return _request(user_input, HTTPSConnection, "putrequest", False)


@mock_connection
def _request_init(user_input, connection_class):
    try:
        c = connection_class(user_input)
        c.request(TRUSTED_METHOD, TRUSTED_URL)
        return c.getresponse().status
    except Exception:
        return EXCEPTION_CODE


def do_httpconnection_init(user_input):
    return _request_init(user_input, HTTPConnection)


def do_httpsconnection_init(user_input):
    return _request_init(user_input, HTTPSConnection)
