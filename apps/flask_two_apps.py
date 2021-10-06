import os

from flask import Flask

from vulnpy.flask.blueprint import vulnerable_blueprint
from werkzeug.middleware.dispatcher import DispatcherMiddleware


primary_app = Flask(__name__ + "-primary")

app1 = Flask(__name__ + "-1")
app1.register_blueprint(vulnerable_blueprint)


app2 = Flask(__name__ + "-2")
app2.register_blueprint(vulnerable_blueprint)


@app1.route("/")
def frontend():
    return "<p>Frontend app 1 </p>"


@app2.route("/")
def backend():
    return "<p>Backend app 2 </p>"


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.flask import ContrastMiddleware

    app1.wsgi_app = ContrastMiddleware(app1)
    app2.wsgi_app = ContrastMiddleware(app2)

    primary_app.wsgi_app = DispatcherMiddleware(
        primary_app.wsgi_app, {"/app1": app1.wsgi_app, "/app2": app2.wsgi_app}
    )

    combined_app = primary_app
