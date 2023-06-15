from aiohttp import web
from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger


def _get_user_input(request):
    return request.rel_url.query.get("user_input", "")


def gen_root_view(name):
    async def _root_view(request):
        template = get_template("{}.html".format(name))
        return web.Response(text=template, content_type="text/html")

    return _root_view


def get_trigger_view(name, trigger):
    async def _view(request):
        user_input = _get_user_input(request)
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return web.Response(text=template, content_type="text/html")

    return _view


def get_root_name(name):
    if name == "home":
        return "/vulnpy"
    return "/vulnpy/{}".format(name)


def get_trigger_name(name, trigger):
    return "/vulnpy/{}/{}".format(name, trigger)


def generate_root_urls():
    root_urls = []
    for name in TRIGGER_MAP:
        view_name = get_root_name(name)
        view_func = gen_root_view(name)
        setattr(view_func, "__name__", view_name)

        root_urls.append(web.get(view_name, view_func))
        # aiohttp doesn't have automatic redirect if trailing slash is added
        # so assigning the same view_func to two views will
        # work for either case
        root_urls.append(web.get(view_name + "/", view_func))

    return root_urls


def generate_trigger_urls():
    trigger_urls = []

    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)
            view_func = get_trigger_view(name, trigger)

            setattr(view_func, "__name__", view_name)
            trigger_urls.append(web.get(view_name, view_func))
            trigger_urls.append(web.get(view_name + "/", view_func))

    return trigger_urls


vulnerable_routes = generate_root_urls() + generate_trigger_urls()
