# VulnPy

A library of purposely-vulnerable Python functions. These serve as a foundation for creating
insecure web applications, to be used for security testing and demonstration.

**WARNING: Do not use this library in a production environment!**

## Installation

VulnPy contains both standalone functions and plug-and-play API extensions to various popular
Python web frameworks. To use vulnpy with your web framework, be sure to install this package with
the appropriate extra dependencies specified - detailed below.

### Flask

Install vulnpy with flask extensions:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[flask]'
```

When setting up your application, register the vulnerable blueprint to your `Flask` application
object:

```py
from vulnpy.flask import vulnerable_blueprint

app = Flask(__name__)
app.register_blueprint(vulnerable_blueprint)
```

### Django

Install vulnpy with django extensions:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[django]'
```

Add vulnpy's routes to your `urlpatterns` sequence (in the module specified by the ROOT_URLCONF
setting). For example:

```py
from vulnpy.django import vulnerable_urlpatterns

urlpatterns = [
	path('example/', views.example),
    # ... etc
] + vulnerable_urlpatterns
```

`vulnpy.django.vulnerable_urlpatterns` is a list of paths.


### Pyramid

Install vulnpy with pyramid extensions:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[pyramid]'
```

During application configuration, include vulnpy's vulnerable routes:

```py
config = Configurator()
config.include("vulnpy.pyramid.vulnerable_routes")
```

### Falcon

Install vulnpy with falcon extensions:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[falcon]'
```

Use the `add_vulnerable_routes` function to register vulnpy's routes with your `Falcon.API`
application object:

```py
import vulnpy.falcon

app = Falcon.API()
vulnpy.falcon.add_vulnerable_routes(app)
```

### WSGI

Install vulnpy with wsgi extensions:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[wsgi]'
```

`vulnpy.wsgi.vulnerable_app` is a vulnerable WSGI application. This versatile component
can be used with a variety of frameworks. For example, Pylons provides a `Cascade` class,
which can be used to compose WSGI applications serially.

## Sample Servers

`vulnpy` is intended to extend the functionality of an existing web application. However, for
convenience, we provide tiny webapps for each supported framework with `vulnpy` attached.

To serve a webapp on your local machine,
- check out the source repo and `cd` into it
- ensure that vulnpy is installed in your current virtual environment with the appropriate extensions (see above)
- run:

```sh
make (your_framework)
```

For example, `pip install -e ".[flask]" && make flask` launches a simple flask webapp with vulnpy
endpoints.

### Note on SSRF

By default, SSRF requests (requests made by the webserver to a third party) are mocked out, meaning
vulnpy will not send real requests when invoking SSRF endpoints. To disable this behavior and
enable vulnpy to send real network requests, set the VULNPY_REAL_SSRF_REQUESTS to any nonzero value.
The reason for this is simply to avoid accidentally overwhelming a third-party server when testing.

Vulnpy's sample web applications make use of this option.
