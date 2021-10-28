from aiohttp import web

from vulnpy.aiohttp import vulnerable_routes

routes = web.RouteTableDef()


@routes.get("/")
def index(request):
    raise web.HTTPFound("/vulnpy")


def init_app(argv):
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(vulnerable_routes)

    return app


if __name__ == "__main__":
    web.run_app(init_app())
