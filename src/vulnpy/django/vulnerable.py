from django.http import HttpResponse

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from vulnpy.common import get_template
from vulnpy.trigger import cmdi


def _vulnpy_root(request):
    return HttpResponse(get_template("home.html"))


def _cmdi(request):
    return HttpResponse(get_template("cmdi.html"))


def _cmdi_os_system(request):
    user_input = _get_user_input(request)
    cmdi.do_os_system(user_input)
    return HttpResponse(get_template("cmdi.html"))


def _cmdi_subprocess_popen(request):
    user_input = _get_user_input(request)
    cmdi.do_subprocess_popen(user_input)
    return HttpResponse(get_template("cmdi.html"))


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


vulnerable_urlpatterns = [
    compat_url(r"^vulnpy/?$", _vulnpy_root),
    compat_url(r"^vulnpy/cmdi/?$", _cmdi),
    compat_url(r"^vulnpy/cmdi/os-system/?$", _cmdi_os_system),
    compat_url(r"^vulnpy/cmdi/subprocess-popen/?$", _cmdi_subprocess_popen),
]

# This module can also be used as a standalone ROOT_URLCONF
urlpatterns = vulnerable_urlpatterns
