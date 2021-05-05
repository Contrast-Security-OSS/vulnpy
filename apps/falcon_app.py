from binascii import hexlify
from hashlib import md5
import os

import falcon
import vulnpy.falcon


MIDDLEWARE = []
if os.environ.get("VULNPY_FALCON_MULTIPART_MIDDLEWARE"):
    from falcon_multipart.middleware import MultipartMiddleware

    MIDDLEWARE.append(MultipartMiddleware())


class Index(object):
    def on_get(self, req, resp):
        raise falcon.HTTPFound("/vulnpy")


class FileUpload(object):
    def on_post(self, req, resp):
        user_input = req._params["upload"].file.read()

        digest = hexlify(md5(user_input).digest()).decode("utf8")

        cmd = "echo " + str(user_input[:10])
        os.system(cmd)

        resp.status = falcon.HTTP_200
        resp.media = {"status": "ok", "md5": digest}


app = falcon.API(middleware=MIDDLEWARE)
vulnpy.falcon.add_vulnerable_routes(app)
app.add_route("/", Index())
app.add_route("/file-upload", FileUpload())

if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.falcon import ContrastMiddleware

    app = ContrastMiddleware(app)
