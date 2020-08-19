import os

import falcon
import vulnpy.falcon


class Index(object):
    def on_get(self, req, resp):
        raise falcon.HTTPFound("/vulnpy")


app = falcon.API()
vulnpy.falcon.add_vulnerable_routes(app)
app.add_route("/", Index())

if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.agent.middlewares.wsgi_middleware import (
        WSGIMiddleware as ContrastMiddleware,
    )

    app = ContrastMiddleware(app)
