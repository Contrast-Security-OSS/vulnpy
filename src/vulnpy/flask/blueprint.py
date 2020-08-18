from flask import Blueprint, request

from vulnpy.common import get_template
from vulnpy.trigger import cmdi

vulnerable_blueprint = Blueprint("vulnpy", __name__, url_prefix="/vulnpy",)


@vulnerable_blueprint.route("/", methods=["GET", "POST"], strict_slashes=False)
def _home():
    return get_template("home.html")


@vulnerable_blueprint.route("/cmdi/", methods=["GET", "POST"], strict_slashes=False)
def _cmdi():
    return get_template("cmdi.html")


@vulnerable_blueprint.route(
    "/cmdi/os-system/", methods=["GET", "POST"], strict_slashes=False
)
def _cmdi_os_system():
    user_input = _get_user_input()
    cmdi.do_os_system(user_input)
    return get_template("cmdi.html")


@vulnerable_blueprint.route(
    "/cmdi/subprocess-popen/", methods=["GET", "POST"], strict_slashes=False
)
def _cmdi_subprocess_popen():
    user_input = _get_user_input()
    cmdi.do_subprocess_popen(user_input)
    return get_template("cmdi.html")


def _get_user_input():
    if request.method == "GET":
        return request.args.get("user_input", "")
    return request.form.get("user_input", "")
