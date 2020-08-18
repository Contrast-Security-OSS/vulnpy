import os
import sys

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
    settings.configure(ROOT_URLCONF=filename, ALLOWED_HOSTS="localhost")
    execute_from_command_line(sys.argv)
