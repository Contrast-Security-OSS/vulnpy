import os
import sys

from quart import Quart, redirect
from vulnpy.quart import vulnerable_blueprint

app = Quart(__name__)
app.register_blueprint(vulnerable_blueprint)


@app.route("/")
async def index():
    return redirect("/vulnpy/")


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.quart import ContrastMiddleware

    app.asgi_app = ContrastMiddleware(app)


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    app.run(host, port)
