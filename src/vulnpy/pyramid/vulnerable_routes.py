from pyramid.response import Response

from vulnpy.trigger import cmdi


def _home(request):
    return Response("vulnpy root")


def _cmdi_os_system(request):
    user_input = _get_user_input(request)
    status = cmdi.do_os_system(user_input)
    return Response(str(status))


def _cmdi_subprocess_popen(request):
    user_input = _get_user_input(request)
    split_user_input = user_input.split()
    try:
        output = cmdi.do_subprocess_popen(split_user_input)
    except Exception as e:
        return Response(str(e), 400)
    return Response(output)


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


def includeme(config):
    """
    config.include looks for a function with this name specifically
    """
    config.add_route("vulnpy-root", "")
    config.add_view(_home, route_name="vulnpy-root")
    config.add_route("cmdi-os-system", "/cmdi/os-system")
    config.add_view(_cmdi_os_system, route_name="cmdi-os-system")
    config.add_route("cmdi-subprocess-popen", "/cmdi/subprocess-popen")
    config.add_view(_cmdi_subprocess_popen, route_name="cmdi-subprocess-popen")
