import os
from pathlib import Path

from flask import Blueprint, Flask, redirect, request
from jinja2 import Environment, FileSystemLoader

from vulnpy.flask.blueprint import vulnerable_blueprint


loader = FileSystemLoader(Path(__file__).parent / "templates" / "jinja")
environment = Environment(loader=loader)

template_blueprint = Blueprint("template-xss", __name__, url_prefix="/template-xss")


@template_blueprint.get("/jinja")
def jinja_xss():
    template = environment.get_template("xss.html")
    return template.render(
        path="/template-xss/jinja", user_input=request.args.get("user_input", "")
    )


app = Flask(__name__)
app.register_blueprint(vulnerable_blueprint)
app.register_blueprint(template_blueprint)


app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False


@app.route("/")
def index():
    return redirect("/vulnpy/")


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.flask import ContrastMiddleware

    app.wsgi_app = ContrastMiddleware(app)
