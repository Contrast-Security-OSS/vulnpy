import os

from flask import Flask, redirect

from vulnpy.flask.blueprint import vulnerable_blueprint
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app1 = Flask(__name__)
app1.register_blueprint(vulnerable_blueprint)


app2 = Flask(__name__)
app2.register_blueprint(vulnerable_blueprint)

@app1.route("/")
def frontend():
    breakpoint()
    return redirect("/vulnpy/")


@app1.route("/backend")
def backend():
    breakpoint()
    return redirect("/vulnpy/")


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.flask import ContrastMiddleware

    app1.wsgi_app = ContrastMiddleware(app1)
    app2.wsgi_app = ContrastMiddleware(app2)

    combined_app = DispatcherMiddleware(app1, {
        '/app2': app2
    })
    combined_app = combined_app.app
