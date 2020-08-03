from vulnpy.trigger import cmdi

from flask import Blueprint, request

vulnerable_blueprint = Blueprint("vulnpy", __name__, url_prefix="/vulnpy")


@vulnerable_blueprint.route("/", methods=["GET", "POST"])
def _home():
    return "vulnpy root"


@vulnerable_blueprint.route("/cmdi/os-system/", methods=["GET", "POST"])
def _cmdi_os_system():
    user_input = _get_user_input()
    status = cmdi.do_os_system(user_input)
    return str(status)


@vulnerable_blueprint.route("/cmdi/subprocess-popen/", methods=["GET", "POST"])
def _cmdi_subprocess_popen():
    user_input = _get_user_input()
    output = cmdi.do_subprocess_popen(user_input)
    return output


def _get_user_input():
    if request.method == "GET":
        return request.args.get("user_input", "")
    return request.form.get("user_input", "")
