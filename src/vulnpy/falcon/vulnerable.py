from vulnpy.common import get_template
from vulnpy.trigger import cmdi


def add_vulnerable_routes(app):
    """
    Add vulnpy's routes to the provided falcon app.
    Also enables stripping of trailing URL slashes for the entire application.
    This means that /foo/bar and /foo/bar/ will resolve to the same handler.
    :param app: instance of falcon.API
    """
    app.req_options.strip_url_path_trailing_slash = True
    app.add_route("/vulnpy", Home())
    app.add_route("/vulnpy/cmdi", Cmdi())
    app.add_route("/vulnpy/cmdi/os-system", OsSystem())
    app.add_route("/vulnpy/cmdi/subprocess-popen", SubprocessPopen())


def _set_response(resp, path):
    """
    Set the response body and Content-Type
    """
    resp.body = get_template(path)
    resp.content_type = "text/html"


class Home(object):
    def on_get(self, req, resp):
        _set_response(resp, "home.html")


class Cmdi(object):
    def trigger(self, command):
        pass

    def on_get(self, req, resp):
        user_input = req.get_param("user_input") or ""
        catch_exception = req.get_param_as_bool("catch_exception")

        if catch_exception:
            try:
                self.trigger(user_input)
            except Exception:
                pass
        else:
            self.trigger(user_input)

        _set_response(resp, "cmdi.html")


class OsSystem(Cmdi):
    def trigger(self, command):
        cmdi.do_os_system(command)


class SubprocessPopen(Cmdi):
    def trigger(self, command):
        cmdi.do_subprocess_popen(command)
