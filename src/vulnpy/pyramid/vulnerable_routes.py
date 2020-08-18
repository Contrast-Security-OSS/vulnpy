from pyramid.response import Response

from vulnpy.common import get_template
from vulnpy.trigger import cmdi


def _home(request):
    return Response(get_template("home.html"))


def _cmdi(request):
    return Response(get_template("cmdi.html"))


def _cmdi_os_system(request):
    user_input = _get_user_input(request)
    cmdi.do_os_system(user_input)
    return Response(get_template("cmdi.html"))


def _cmdi_subprocess_popen(request):
    user_input = _get_user_input(request)
    cmdi.do_subprocess_popen(user_input)
    return Response(get_template("cmdi.html"))


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


def includeme(config):
    """
    config.include looks for a function with this name specifically
    """
    _add_route(config, "vulnpy-root", "/vulnpy", _home)
    _add_route(config, "cmdi", "/vulnpy/cmdi", _cmdi)
    _add_route(config, "cmdi-os-system", "/vulnpy/cmdi/os-system", _cmdi_os_system)
    _add_route(
        config,
        "cmdi-subprocess-popen",
        "/vulnpy/cmdi/subprocess-popen",
        _cmdi_subprocess_popen,
    )


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
