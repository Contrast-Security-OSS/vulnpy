from vulnpy.trigger import cmdi

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from django.http import HttpResponse


def _vulnpy_root(request):
    return HttpResponse("vulnpy root")


def _cmdi_os_system(request):
    user_input = _get_user_input(request)
    status = cmdi.do_os_system(user_input)
    return HttpResponse(str(status))


def _cmdi_subprocess_popen(request):
    user_input = _get_user_input(request)
    output = cmdi.do_subprocess_popen(user_input)
    return HttpResponse(output)


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


vulnerable_urlpatterns = [
    compat_url(r"^vulnpy/?$", _vulnpy_root),
    compat_url(r"^vulnpy/cmdi/os-system/?$", _cmdi_os_system),
    compat_url(r"^vulnpy/cmdi/subprocess-popen/?$", _cmdi_subprocess_popen),
]

# This module can also be used as a standalone ROOT_URLCONF
urlpatterns = vulnerable_urlpatterns
