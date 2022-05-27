import os
import falcon.asgi
import vulnpy.falcon


class Index(object):
    async def on_get(self, req, resp):
        raise falcon.HTTPFound("/vulnpy")


app = falcon.asgi.App()
vulnpy.falcon.add_vulnerable_asgi_routes(app)
app.add_route("/", Index())


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.falcon_asgi import ContrastMiddleware

    app = ContrastMiddleware(app)
