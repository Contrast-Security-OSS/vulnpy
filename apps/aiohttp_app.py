from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def hello(request):
    return web.Response(text="Hello, world")


def init_app(argv):
    app = web.Application()
    app.add_routes(routes)  # vulnerable routes
    return app


if __name__ == "__main__":
    web.run_app(init_app())
