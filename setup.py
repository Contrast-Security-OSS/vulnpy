import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md")) as f:
        README = f.read()
except IOError:
    README = ""

trigger_extras = {"PyYAML<6", "lxml>=4.3.1", "mock==3.*"}
aiohttp_extras = {
    "aiohttp==3.7.*; python_version >= '3.7'",
    "aiohttp-jinja2==1.5.*; python_version >= '3.7'",
} | trigger_extras
django_extras = {"Django<4"} | trigger_extras
falcon_extras = {"falcon<4", "falcon-multipart==0.2.0"} | trigger_extras
flask_extras = {"Flask<3"} | trigger_extras
fastapi_extras = {
    "fastapi<=0.70; python_version >= '3.6'",
    "uvicorn[standard]; python_version >= '3.6'",
    "python-multipart<1",
} | trigger_extras
gunicorn_max_extras = {
    "gunicorn<20.1; python_version < '3.6'",
    "gunicorn==20.1.*; python_version >= '3.6'",
}
uwsgi_max_extras = {"uwsgi==2.0.*"}
uwsgi_min_extras = {"uwsgi==2.0.14"}
gunicorn_min_extras = {"gunicorn==0.16.1"}
pyramid_extras = {"pyramid<2", "waitress<2.1"} | trigger_extras

wsgi_extras = trigger_extras
bottle_extras = {"bottle<1"} | trigger_extras

dev_extras = {"WebTest==2.0.*", "tox==3.*"}

all_extras = (
    trigger_extras
    | aiohttp_extras
    | django_extras
    | falcon_extras
    | flask_extras
    | pyramid_extras
    | wsgi_extras
    | dev_extras
    | bottle_extras
    | uwsgi_max_extras
    | fastapi_extras
    | gunicorn_max_extras
)

setup(
    name="vulnpy",
    version="0.1.0",
    description="Purposely-vulnerable functions for application security testing",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="security testing",
    author="Contrast Security, Inc.",
    author_email="python@contrastsecurity.com",
    url="https://github.com/Contrast-Security-OSS/vulnpy",
    license="MIT",
    include_package_data=True,
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    extras_require={
        "all": all_extras,
        "aiohttp": aiohttp_extras,
        "django": django_extras,
        "falcon": falcon_extras,
        "flask": flask_extras,
        "fastapi": fastapi_extras,
        "pyramid": pyramid_extras,
        "bottle": bottle_extras,
        "wsgi": wsgi_extras,
        "trigger": trigger_extras,
        "uwsgi-max": uwsgi_max_extras,
        "uwsgi-min": uwsgi_min_extras,
        "gunicorn-max": gunicorn_max_extras,
        "gunicorn-min": gunicorn_min_extras,
    },
)
