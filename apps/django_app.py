import os
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import redirect

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from vulnpy.django import vulnerable_urlpatterns


urlpatterns = [
    compat_url(r"^$", lambda r: redirect("/vulnpy"))
] + vulnerable_urlpatterns

filename = os.path.basename(os.path.splitext(__file__)[0])

if __name__ == "__main__":

    options = {
        "ROOT_URLCONF": filename,
        "ALLOWED_HOSTS": ["localhost", "127.0.0.1", "[::1]"],
    }

    if os.environ.get("VULNPY_USE_CONTRAST"):
        # TODO: be able to import as "contrast.django.ContrastMiddleware"
        if django.VERSION < (1, 10):
            middleware_setting_name = "MIDDLEWARE_CLASSES"
            contrast_middleware_name = (
                "contrast.agent.middlewares.legacy_django_middleware.DjangoMiddleware"
            )
        else:
            middleware_setting_name = "MIDDLEWARE"
            contrast_middleware_name = (
                "contrast.agent.middlewares.django_middleware.DjangoMiddleware"
            )
        options[middleware_setting_name] = [contrast_middleware_name]

    settings.configure(**options)
    execute_from_command_line(sys.argv)
