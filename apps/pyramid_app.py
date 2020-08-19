import os
import sys

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from waitress import serve


def index(request):
    return HTTPFound(location="/vulnpy")


if __name__ == "__main__":
    host, port = sys.argv[1].split(":")
    with Configurator() as config:
        config.include("vulnpy.pyramid.vulnerable_routes")
        config.add_route("index", "/")
        config.add_view(index, route_name="index")

        if os.environ.get("VULNPY_USE_CONTRAST"):
            config.add_tween(
                "contrast.agent.middlewares.pyramid_middleware.PyramidMiddleware"
            )

        app = config.make_wsgi_app()

    serve(app, host=host, port=int(port))
