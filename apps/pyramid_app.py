from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from waitress import serve


def index(request):
    return HTTPFound(location="/vulnpy")


if __name__ == "__main__":
    with Configurator() as config:
        config.include("vulnpy.pyramid.vulnerable_routes")
        config.add_route("index", "/")
        config.add_view(index, route_name="index")
        app = config.make_wsgi_app()
    serve(app, host="localhost", port=8000)
