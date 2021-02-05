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


if __name__ == "__main__":
    run(app=StripPathMiddleware(app))
