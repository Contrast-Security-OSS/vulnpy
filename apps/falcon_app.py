import falcon
import vulnpy.falcon


class Index(object):
    def on_get(self, req, resp):
        raise falcon.HTTPFound("/vulnpy")


app = falcon.API()
vulnpy.falcon.add_vulnerable_routes(app)
app.add_route("/", Index())
