from aiohttp import web
import aiohttp_jinja2
import jinja2

from vulnpy.aiohttp import vulnerable_routes


def init_app(argv):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("src/vulnpy/templates/"))
    app.add_routes(vulnerable_routes)
    return app


if __name__ == "__main__":
    web.run_app(init_app())
