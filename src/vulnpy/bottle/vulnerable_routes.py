from bottle import request
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


def gen_root_view(name):
    def _root_view():
        return get_template("{}.html".format(name))

    return _root_view


def get_trigger_name(name, trigger):
    return "/vulnpy/{}/{}".format(name, trigger)


def get_trigger_view(name, trigger):
    def _root_view():
        user_input = _get_user_input(request)
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)
        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return template

    return _root_view


def generate_root_urls(app):
    for name in TRIGGER_MAP:
        view_name = get_root_pattern(name)
        view_func = gen_root_view(name)

        app.route(view_name, ["GET", "POST"], callback=view_func)


def generate_trigger_urls(app):
    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)
            view_func = get_trigger_view(name, trigger)

            app.route(view_name, ["GET", "POST"], callback=view_func)


def add_vulnerable_routes(app):
    generate_root_urls(app)
    generate_trigger_urls(app)
