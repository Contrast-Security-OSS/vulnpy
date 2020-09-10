from django.http import HttpResponse

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from vulnpy.common import get_template
from vulnpy.trigger import cmdi, deserialization


def _cmdi_os_system(request):
    user_input = _get_user_input(request)
    cmdi.do_os_system(user_input)
    return HttpResponse(get_template("cmdi.html"))


def _cmdi_subprocess_popen(request):
    user_input = _get_user_input(request)
    cmdi.do_subprocess_popen(user_input)
    return HttpResponse(get_template("cmdi.html"))


def _deserialization_pickle_load(request):
    user_input = _get_user_input(request)
    deserialization.do_pickle_load(user_input)
    return HttpResponse(get_template("deserialization.html"))


def _deserialization_pickle_loads(request):
    user_input = _get_user_input(request)
    deserialization.do_pickle_loads(user_input)
    return HttpResponse(get_template("deserialization.html"))


def _deserialization_yaml_load(request):
    user_input = _get_user_input(request)
    deserialization.do_yaml_load(user_input)
    return HttpResponse(get_template("deserialization.html"))


def _deserialization_yaml_load_all(request):
    user_input = _get_user_input(request)
    deserialization.do_yaml_load_all(user_input)
    return HttpResponse(get_template("deserialization.html"))


def _get_user_input(request):
    if request.method == "GET":
        return request.GET.get("user_input", "")
    return request.POST.get("user_input", "")


def gen_root_view(name="home"):
    def _root(request):
        return HttpResponse(get_template("{}.html".format(name)))

    return _root


def get_root_name(name):
    if name == "home":
        return r"^vulnpy/?$"
    return r"^vulnpy/{}/?$".format(name)


VIEW_NAMES = [
    "home",
    "cmdi",
    "deserialization",
]


root_urls = []
for name in VIEW_NAMES:
    view_name = get_root_name(name)
    view_func = gen_root_view(name)

    root_urls.append(compat_url(view_name, view_func))


vulnerable_urlpatterns = [
    compat_url(r"^vulnpy/cmdi/os-system/?$", _cmdi_os_system),
    compat_url(r"^vulnpy/cmdi/subprocess-popen/?$", _cmdi_subprocess_popen),
    compat_url(r"^vulnpy/deserialization/pickle-load/?$", _deserialization_pickle_load),
    compat_url(
        r"^vulnpy/deserialization/pickle-loads/?$", _deserialization_pickle_loads
    ),
    compat_url(r"^vulnpy/deserialization/yaml-load/?$", _deserialization_yaml_load),
    compat_url(
        r"^vulnpy/deserialization/yaml-load-all/?$", _deserialization_yaml_load_all
    ),
] + root_urls

# This module can also be used as a standalone ROOT_URLCONF
urlpatterns = vulnerable_urlpatterns
