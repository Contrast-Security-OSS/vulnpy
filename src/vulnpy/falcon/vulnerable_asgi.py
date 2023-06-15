import inspect
import sys
from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger


def get_root_name(name):
    if name == "home":
        return "/vulnpy"
    return "/vulnpy/{}".format(name)


def get_trigger_name(name, trigger):
    return "/vulnpy/{}/{}".format(name, trigger)


def gen_root_view(name):  # noqa: C901
    if name == "home":

        class _View(object):
            async def on_get(self, req, resp):
                _set_response(resp, "{}.html".format(name))

    else:

        class _View(object):
            def trigger(self, command):
                pass

            async def on_get(self, req, resp):
                user_input = req.get_param("user_input") or ""
                catch_exception = req.get_param_as_bool("catch_exception")

                if catch_exception:
                    try:
                        self.trigger(user_input)
                    except Exception:
                        pass
                else:
                    self.trigger(user_input)

                if name == "xss":
                    _set_xss_response(resp, "{}.html".format(name), user_input)
                else:
                    _set_response(resp, "{}.html".format(name))

    return _View


def find_base_class(name):
    """
    Find a class LIKE name currently defined in this module.

    :param name: str
    :return: class matching "name"
    """
    current_module = sys.modules[__name__]

    for obj_name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and obj_name == name.title():
            return obj


def get_trigger_view(name, trigger):
    baseclass = find_base_class(name)

    class _View(baseclass):
        def trigger(self, command):
            trigger_func = get_trigger(name, trigger)

            if trigger_func:
                trigger_func(command)

    return _View


def generate_root_urls(app):
    for name in TRIGGER_MAP:
        view_name = get_root_name(name)
        view_cls = gen_root_view(name)

        # Add the view class to the current module to be able to retrieve later
        current_module = sys.modules[__name__]
        setattr(current_module, name.title(), view_cls)

        app.add_route(view_name, view_cls())


def generate_trigger_urls(app):
    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)

            view_cls = get_trigger_view(name, trigger)

            app.add_route(view_name, view_cls())


def add_vulnerable_asgi_routes(app):
    """
    Add vulnpy's routes to the provided falcon app.
    Also enables stripping of trailing URL slashes for the entire application.
    This means that /foo/bar and /foo/bar/ will resolve to the same handler.
    :param app: instance of falcon.API
    """
    app.req_options.strip_url_path_trailing_slash = True

    # Root urls must be generated before trigger urls.
    generate_root_urls(app)
    generate_trigger_urls(app)


def _set_response(resp, path):
    """
    Set the response body and Content-Type
    """
    resp.text = get_template(path)
    resp.content_type = "text/html"


def _set_xss_response(resp, path, user_input):
    template = get_template(path)
    template += "<p>XSS: " + user_input + "</p>"

    resp.text = template
    resp.content_type = "text/html"
