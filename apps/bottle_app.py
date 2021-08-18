import os
import sys
from bottle import Bottle, run, redirect
from vulnpy.bottle import add_vulnerable_routes


app = Bottle(__name__)
add_vulnerable_routes(app)


@app.route("/")
def index():
    redirect("/vulnpy")


class StripPathMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ["PATH_INFO"] = environ["PATH_INFO"].rstrip("/")
        return self.app(environ, start_response)


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.bottle import ContrastMiddleware

    app = ContrastMiddleware(app)

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    run(app=StripPathMiddleware(app), host=host, port=port)
