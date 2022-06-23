from django.http import HttpResponse
import django
import urllib.parse

try:
    from django.conf.urls import url as compat_url
except ImportError:
    from django.urls import re_path as compat_url

from vulnpy.common import get_template
from vulnpy.trigger import TRIGGER_MAP, get_trigger


async def _get_user_input(request):
    # Django 3.* doesn't have a body for GET requests
    # and adds the body to the header instead
    # so we need to check the version and decode the url
    if (
        request.method == "GET"
        and django.VERSION[0] < 4
        and not request.GET.get("user_input")
    ):
        header_user_input = request.META.get("HTTP_QUERY_STRING")
        return urllib.parse.unquote(header_user_input.split("=", 1)[1])

    if request.method == "GET":
        return request.GET.get("user_input", "")

    # We need this to bypass request.POST not being initialized
    # calling request.body triggers process_view which initializes request.POST
    if request.body:
        return request.POST.get("user_input", "")


def gen_root_view(name):
    async def _root(request):
        return HttpResponse(get_template("{}.html".format(name)))

    return _root


def get_trigger_view(name, trigger):
    async def _view(request):
        user_input = await _get_user_input(request)
        trigger_func = get_trigger(name, trigger)

        if trigger_func:
            trigger_func(user_input)

        template = get_template("{}.html".format(name))

        if name == "xss" and trigger == "raw":
            template += "<p>XSS: " + user_input + "</p>"

        return HttpResponse(template)

    return _view


def get_root_name(name):
    if name == "home":
        return r"^vulnpy/?$"
    return r"^vulnpy/{}/?$".format(name)


def get_trigger_name(name, trigger):
    return r"^vulnpy/{}/{}/?$".format(name, trigger)


def generate_root_urls():
    root_urls = []
    for name in TRIGGER_MAP:
        view_name = get_root_name(name)
        view_func = gen_root_view(name)

        root_urls.append(compat_url(view_name, view_func))

    return root_urls


def generate_trigger_urls():
    trigger_urls = []

    for name, triggers in TRIGGER_MAP.items():
        for trigger in triggers:
            view_name = get_trigger_name(name, trigger)
            view_func = get_trigger_view(name, trigger)

            trigger_urls.append(compat_url(view_name, view_func))

    return trigger_urls


vulnerable_asgi_urlpatterns = generate_root_urls() + generate_trigger_urls()

# This module can also be used as a standalone ROOT_URLCONF
urlpatterns = vulnerable_asgi_urlpatterns
