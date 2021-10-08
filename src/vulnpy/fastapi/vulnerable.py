from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from vulnpy.common import get_template

from vulnpy.trigger import TRIGGER_MAP, get_trigger


router = APIRouter(prefix="/vulnpy",)


def get_root_name(name):
    if name == "home":
        return "/"
    return "/{}/".format(name)


def get_trigger_name(name, trigger):
    return "/{}/{}/".format(name, trigger)


def gen_root_view(name):
    view_name = get_root_name(name)

    @router.get(path=view_name, name=view_name)
    async def _view():
        return HTMLResponse(get_template("{}.html".format(name)))


def get_trigger_view(name, trigger):
    view_name = get_trigger_name(name, trigger)

    @router.get(path=view_name, name=view_name)
    async def _view(user_input: str):
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return HTMLResponse(template)


def get_trigger_view_sync(name, trigger):
    view_name = get_trigger_name(name, trigger) + "threadpool"

    @router.get(path=view_name, name=view_name)
    def _sync_view(user_input: str):
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return HTMLResponse(template)


def generate_root_urls():
    for name in TRIGGER_MAP:
        gen_root_view(name)


def generate_trigger_urls():
    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            get_trigger_view(name, trigger)
            get_trigger_view_sync(name, trigger)


generate_root_urls()
generate_trigger_urls()
