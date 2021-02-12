from pyramid.response import Response

from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


def get_root_pattern(name):
    if name == "home":
        return "/vulnpy"
    return "/vulnpy/{}".format(name)


def get_trigger_pattern(name, trigger):
    return "/vulnpy/{}/{}".format(name, trigger)


def get_root_name(name):
    if name == "home":
        return "vulnpy-root"
    return "vulnpy-{}".format(name)


def get_trigger_name(name, trigger):
    return "vulnpy-{}-{}".format(name, trigger)


def gen_root_view(name):
    def _root(request):
        return Response(get_template("{}.html".format(name)))

    return _root


def get_trigger_view(name, trigger):
    def _view(request):
        user_input = _get_user_input(request)
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return Response(template)

    return _view


def generate_root_urls(config):
    for name in TRIGGER_MAP:
        view_name = get_root_name(name)
        view_pattern = get_root_pattern(name)
        view_func = gen_root_view(name)
        _add_route(config, view_name, view_pattern, view_func)


def generate_trigger_urls(config):
    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)
            view_pattern = get_trigger_pattern(name, trigger)
            view_func = get_trigger_view(name, trigger)

            _add_route(config, view_name, view_pattern, view_func)


def _add_route(config, route_name, pattern, view):
    """
    Adds a view to the config called route_name using the specified URL pattern.
    Also adds an identical handler for the trailing slash case.
    :param config: instance of pyramid.config.Configurator
    :param route_name: name given to the route
    :param pattern: URL pattern
    :param view: callable that will handle the view
    """
    config.add_route(route_name, pattern)
    config.add_view(view, route_name=route_name)

    route_name_slash = route_name + "-with-slash"
    config.add_route(route_name_slash, pattern + "/")
    config.add_view(view, route_name=route_name_slash)


def includeme(config):
    """
    config.include looks for a function with this name specifically
    """
    generate_root_urls(config)
    generate_trigger_urls(config)
