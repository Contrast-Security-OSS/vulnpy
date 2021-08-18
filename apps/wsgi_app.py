import os
import sys
from wsgiref.simple_server import make_server

from vulnpy.wsgi import vulnerable_app


def rerouter_middleware(app):
    """
    Reroute the root page to /vulnpy/. This is slightly irresponsible because we
    don't call the wrapped application in this case.
    """

    def wrapped_application(environ, start_response):
        if environ["PATH_INFO"] in ("", "/"):
            start_response("302 FOUND", [("Location", "/vulnpy/")])
            return [b""]
        return app(environ, start_response)

    return wrapped_application


def make_app():
    app = rerouter_middleware(vulnerable_app)
    if os.environ.get("VULNPY_USE_CONTRAST"):
        from contrast.wsgi import ContrastMiddleware

        app = ContrastMiddleware(app)

    return app


app = make_app()

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    httpd = make_server(host, port, app)
    print("WSGI app starting on http://{}:{}".format(host, port))
    httpd.serve_forever()
