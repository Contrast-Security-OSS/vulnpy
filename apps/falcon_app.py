from binascii import hexlify
from hashlib import md5
import os
import threading
import sys
import falcon
import vulnpy.falcon
import time

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


def thread_function(user_input):
    """This is intented to test Contrast specific functionality!"""

    print("starting background thread")

    # We're testing that a child thread still has a request context
    # even after the parent thread exited, so waiting here so the parent
    # thread has time to exit.
    time.sleep(2)

    try:
        import contrast
        from contrast.agent.settings_state import SettingsState
    except ImportError:
        return

    settings = SettingsState()
    if settings.is_protect_enabled():
        # Presence of context only matters for Protect.
        context = contrast.CS__CONTEXT_TRACKER.current()

        # The goal here is to ensure that a request context
        # still exists in a child thread even if the parent thread exited.
        if context is None:
            # If context is None we will not finish the thread's work.
            print("Context is None")
            sys.exit(1)

    cmd = "echo " + str(user_input)
    os.system(cmd)

    # Do NOT remove this print as it is used in a testing assertion.
    print("finished background thread")


class ThreadView(object):
    def on_get(self, req, resp):
        """View that creates a child thread for some work"""
        user_input = req.get_param("user_input") or ""
        threading.Thread(target=thread_function, args=(user_input,)).start()
        resp.status = falcon.HTTP_200
        resp.body = "Spawned thread"


app = falcon.API(middleware=MIDDLEWARE)
vulnpy.falcon.add_vulnerable_routes(app)
app.add_route("/", Index())
app.add_route("/file-upload", FileUpload())
app.add_route("/thread", ThreadView())


if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.falcon import ContrastMiddleware

    app = ContrastMiddleware(app)
