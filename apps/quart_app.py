import os
import sys

from quart import Quart, redirect, Response, request
from vulnpy.quart import vulnerable_blueprint
from vulnpy.trigger.cmdi import do_os_system

app = Quart(__name__)
app.register_blueprint(vulnerable_blueprint)


@app.route("/")
async def index():
    return redirect("/vulnpy/")


@app.post("/files/upload")
async def upload_return_large_file():
    files = await request.files
    stream = files.get("file")
    user_input = stream.read()
    try:
        do_os_system(user_input[:20])
    except ValueError:
        pass
    return Response(response="success", status=200)


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.quart import ContrastMiddleware

    app.asgi_app = ContrastMiddleware(app)


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    app.run(host, port)
