import sys

from django.conf import settings
from django.core import management
from django.core.asgi import get_asgi_application
from django.shortcuts import redirect

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url
from vulnpy.django import vulnerable_urlpatterns

urlpatterns = [
    compat_url(r"^$", lambda r: redirect("/vulnpy"))
] + vulnerable_urlpatterns

if not settings.configured:
    settings.configure(
        **{
            "ROOT_URLCONF": "django_app"
            if __name__ == "__main__"
            else "apps.django_app",
            "ALLOWED_HOSTS": ["localhost", "127.0.0.1", "[::1]"],
            "ASGI_APPLICATION": "django_app.vulnpy_app",
            "INSTALLED_APPS": [],
        }
    )

vulnpy_app = get_asgi_application()

# todo: add contrast later on
# if os.environ.get("VULNPY_USE_CONTRAST"):
#     from contrast.django import ContrastMiddleware
#
#     vulnpy_app = ContrastMiddleware(vulnpy_app)

if __name__ == "__main__":
    management.execute_from_command_line(sys.argv)
