import os
import sys

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from waitress import serve
from pyramid.events import NewRequest


def index(request):

    # I'm trying to see without putting the headers ( in postman) to this endpoint
    # if when I make a request to it the headers which are
    # ('test-header:oneval', 'second-header:222')
    # are tracked in import.contrast; contrast.STRING_TRACKER
    # but the only way I can see it if i add the headers in postman
    # which then they get tracked but that's because of the request
    breakpoint()
    return HTTPFound(location="/vulnpy")


def setup_post_request(event):

    # this doesn't work for me
    event.request.add_response_callback(breakpoint())


from pyramid.session import SignedCookieSessionFactory

factory = SignedCookieSessionFactory("my session", httponly=True, secure=True)

with Configurator() as config:
    # config.include("vulnpy.pyramid.vulnerable_routes")
    config.add_route("index", "", inherit_slash=True)
    config.add_view(
        index, route_name="index", header=("test-header:oneval", "second-header:222")
    )
    config.set_session_factory(factory)

    if os.environ.get("VULNPY_USE_CONTRAST"):
        # TODO: be able to import as "contrast.pyramid.ContrastMiddleware"
        config.add_tween(
            "contrast.agent.middlewares.pyramid_middleware.PyramidMiddleware"
        )

    app = config.make_wsgi_app()

if __name__ == "__main__":
    host, port = sys.argv[1].split(":")
    serve(app, host=host, port=int(port))
