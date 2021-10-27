from aiohttp import web
import aiohttp_jinja2
from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger


def _get_user_input(request):
    return request.rel_url.query.get("user_input", "")


def gen_root_view(name):
    async def _root_view(request):
        response = aiohttp_jinja2.render_template(
            "{}.html".format(name), request, context={}
        )
        return response

    return _root_view


def get_trigger_view(name, trigger):
    async def _view(request):
        user_input = _get_user_input(request)
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        if name == "xss" and trigger == "raw":
            template = get_template("{}.html".format(name))
            template += "<p>XSS: " + user_input + "</p>"
            response = web.Response(text=template)
        else:
            response = aiohttp_jinja2.render_template(
                "{}.html".format(name), request, context={}
            )
        return response

    return _view


def get_root_name(name):
    if name == "home":
        return "/vulnpy"
    return "/vulnpy/{}".format(name)


def get_trigger_name(name, trigger):
    return "/vulnpy/{}/{}/".format(name, trigger)


def generate_root_urls():
    root_urls = []
    for name in TRIGGER_MAP:
        view_name = get_root_name(name)
        view_func = gen_root_view(name)

        root_urls.append(web.get(view_name, view_func))

    return root_urls


def generate_trigger_urls():
    trigger_urls = []

    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)
            view_func = get_trigger_view(name, trigger)

            trigger_urls.append(web.get(view_name, view_func))

    return trigger_urls


vulnerable_routes = generate_root_urls() + generate_trigger_urls()
