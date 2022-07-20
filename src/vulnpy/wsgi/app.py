from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger, xss
from vulnpy.utils.utils_string import ensure_binary

from urllib.parse import parse_qs


def vulnerable_app(environ, start_response):
    """
    A WSGI application callable that exposes vulnpy's API.

    This application currently only supports user_input coming form
    QUERY_STRING parameters. In the future, it should support form
    submissions.
    """
    response = []
    try:
        name, trigger_func = _get_trigger_info(environ)
    except NotFound:
        return not_found(start_response)

    if trigger_func:
        user_input = _get_user_input(environ)
        trigger_func(user_input)
        if trigger_func is xss.do_raw:
            response.append("<p>XSS: {}</p>".format(user_input))

    response.append(get_template("{}.html".format(name)))
    headers = [("Content-Type", "text/html")]

    # This makes the app vulnerable to cache control missing, since both no-cache and
    # no-store are missing
    headers.append(("Cache-Control", "public"))
    # This makes the app vulnerable to X-XSS-Protection disabled
    headers.append(("X-XSS-Protection", "0"))
    headers.append(("Strict-Transport-Security", "max-age=0"))

    start_response("200 OK", headers)

    return [ensure_binary(s) for s in response]


class NotFound(Exception):
    pass


def not_found(start_response):
    start_response("404 NOT FOUND", [("Content-Type", "text/plain")])
    return [b"The requested page does not exist"]


def _get_user_input(environ):
    """
    Get the user_input param, which must be in the querystring.
    Request body sources are currently unsupported.
    """
    return parse_qs(environ["QUERY_STRING"]).get("user_input", [""])[0]


def _get_trigger_info(environ):
    """
    This method is essentially the router for this application. It gets
    the vulnerability name and trigger function from the request path.
    These two values are returned in a 2-tuple.

    If we find an invalid path, raise a NotFound exception.
    If we find a vulnerability name homepage, such as /vulnpy/cmdi/, the
    second element of the return value will be None.
    """
    path_components = [s for s in environ["PATH_INFO"].split("/") if s != ""]
    if (
        len(path_components) < 1
        or len(path_components) > 3
        or path_components[0] != "vulnpy"
    ):
        raise NotFound()
    if len(path_components) == 1:
        return "home", None

    name = path_components[1]
    if name not in TRIGGER_MAP:
        raise NotFound()
    # we need to do this to avoid path traversal during template resolution
    sanitized_name = [s for s in TRIGGER_MAP.keys() if s == name][0]

    if len(path_components) == 2:
        return sanitized_name, None

    return sanitized_name, _get_trigger_func(sanitized_name, path_components[2])


def _get_trigger_func(name, trigger_name):
    """
    Given a valid vulnerability name, get the trigger function corresponding
    to the vulnerability name and trigger name.

    If the trigger function isn't found, raise NotFound.
    """
    try:
        return get_trigger(name, trigger_name)
    except AttributeError:
        raise NotFound()
