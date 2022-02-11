from quart import Blueprint, request

from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger

vulnerable_blueprint = Blueprint("vulnpy", __name__, url_prefix="/vulnpy")


def _get_user_input():
    if request.headers.get("User_Input") is not None:
        return request.headers.get("User_Input")

    return request.args.get("user_input", "")


def get_root_name(name):
    if name == "home":
        return "/"
    return "/{}/".format(name)


def get_trigger_name(name, trigger):
    return "/{}/{}/".format(name, trigger)


def gen_root_view(name):
    async def _view():
        return get_template("{}.html".format(name))

    view_name = get_root_name(name)
    vulnerable_blueprint.add_url_rule(
        view_name, view_name, _view, methods=["GET", "POST"], strict_slashes=False
    )
    return _view


def generate_root_urls():
    for name in TRIGGER_MAP:
        gen_root_view(name)


def get_trigger_view(name, trigger):
    async def _view():
        user_input = _get_user_input()
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return template

    view_name = get_trigger_name(name, trigger)

    vulnerable_blueprint.add_url_rule(
        view_name, view_name, _view, methods=["GET", "POST"], strict_slashes=False
    )
    return _view


def generate_trigger_urls():
    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            get_trigger_view(name, trigger)


generate_root_urls()
generate_trigger_urls()
