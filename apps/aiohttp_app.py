from aiohttp import web
import os
from vulnpy.aiohttp import vulnerable_routes

routes = web.RouteTableDef()


@routes.get("/")
def index(request):
    raise web.HTTPFound("/vulnpy")


def init_app(argv):
    middlewares = []

    if os.environ.get("VULNPY_USE_CONTRAST"):
        from contrast.aiohttp import ContrastMiddleware

        middlewares = [ContrastMiddleware(app_name="vulnpy app")]

    app = web.Application(middlewares=middlewares)
    app.add_routes(routes)
    app.add_routes(vulnerable_routes)

    return app


if __name__ == "__main__":
    web.run_app(init_app())
