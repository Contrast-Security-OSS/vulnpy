import sys
import os

from django.conf import settings
from django.core import management
from django.core.asgi import get_asgi_application
from django.shortcuts import redirect

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url
import vulnpy.django

urlpatterns = [
    compat_url(r"^$", lambda r: redirect("/vulnpy"))
] + vulnpy.django.vulnerable_asgi_urlpatterns

if not settings.configured:
    settings.configure(
        **{
            "ROOT_URLCONF": "django_asgi_app"
            if __name__ == "__main__"
            else "apps.django_asgi_app",
            "ALLOWED_HOSTS": ["localhost", "127.0.0.1", "[::1]"],
        }
    )

vulnpy_app = get_asgi_application()

if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.django_asgi import ContrastMiddleware

    vulnpy_app = ContrastMiddleware(vulnpy_app)

if __name__ == "__main__":
    management.execute_from_command_line(sys.argv)
