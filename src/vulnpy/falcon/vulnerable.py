from vulnpy.trigger import cmdi


def add_vulnerable_routes(app):
    app.add_route("/vulnpy", Home())
    app.add_route("/vulnpy/cmdi/os-system", OsSystem())
    app.add_route("/vulnpy/cmdi/subprocess-popen", SubprocessPopen())


class Home(object):
    def on_get(self, req, resp):
        resp.body = "vulnpy root"


class Cmdi(object):
    def trigger(self):
        raise NotImplementedError()

    def on_get(self, req, resp):
        user_input = req.get_param("user_input") or ""
        catch_exception = req.get_param_as_bool("catch_exception")

        if catch_exception:
            try:
                result = self.trigger(user_input)
            except Exception as e:
                result = str(e)
        else:
            result = self.trigger(user_input)

        resp.body = result


class OsSystem(Cmdi):
    def trigger(self, command):
        return str(cmdi.do_os_system(command))


class SubprocessPopen(Cmdi):
    def trigger(self, command):
        return cmdi.do_subprocess_popen(command)
