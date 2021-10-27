from aiohttp import web
import aiohttp_jinja2
import jinja2

from vulnpy.aiohttp import vulnerable_routes

routes = web.RouteTableDef()


@routes.get("/")
def index(request):
    raise web.HTTPFound("/vulnpy")


def init_app(argv):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("src/vulnpy/templates/"))

    app.add_routes(routes)
    app.add_routes(vulnerable_routes)

    breakpoint()
    return app


if __name__ == "__main__":
    web.run_app(init_app())
