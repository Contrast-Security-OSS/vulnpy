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
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[flask]'
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
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[django]'
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
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[pyramid]'
```

During application configuration, include vulnpy's vulnerable routes:

```py
config = Configurator()
config.include("vulnpy.pyramid.vulnerable_routes")
```

### Falcon

Install vulnpy with falcon extensions:

```
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[falcon]'
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
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[wsgi]'
```

`vulnpy.wsgi.vulnerable_app` is a vulnerable WSGI application. This versatile component
can be used with a variety of frameworks. For example, Pylons provides a `Cascade` class,
which can be used to compose WSGI applications serially.

### Bottle

Install vulnpy with bottle extensions:

```
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[bottle]'
```

Use the `add_vulnerable_routes` function to register vulnpy's routes with your `bottle`
application:

```py
from bottle import Bottle
from vulnpy.bottle import add_vulnerable_routes

app = Bottle()
add_vulnerable_routes(app)
```

### FastAPI

Install vulnpy with fastapi extensions:

```
pip install 'git+https://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[fastapi]'
```

Use the `include_router` function to register vulnpy's router with your `fastapi`
application:

```py
from fastapi import FastAPI
from vulnpy.fastapi import vulnerable_routes

app = FastAPI()
app.include_router(vulnerable_routes)
```

### Sample Servers

`vulnpy` is intended to extend the functionality of an existing web application. However, for
convenience, we provide tiny webapps for each supported framework with `vulnpy` attached.

#### Running Directly

To serve a webapp on your local machine,
- check out the source repo and `cd` into it
- ensure that vulnpy is installed in your current virtual environment with the appropriate extensions (see above)
- run:

```sh
make (your_framework)
```

For example, `pip install -e ".[flask]" && make flask` launches a simple flask webapp with vulnpy
endpoints.

To run with Contrast, install the agent (`pip install -U contrast-agent`) and set
`VULNPY_USE_CONTRAST=true` before running your desired `make` command.

#### Running Different Servers

While some frameworks come with their own servers, you can use the uWSGI or 
gunicorn servers as well.

`pip install -e ".[flask,uwsgi-max]" && make flask-uwsgi`
launches the flask app with the maximum supported uWSGI version.

`pip install -e ".[falcon,gunicorn-min]" && make falcon-gunicorn`
launches the falcon app with the minimum supported gunicorn version.

#### Running with Contrast in Docker

`vulnpy` provides a Dockerfile that is also preconfigured to enable Contrast Security's
instrumentation. To run a `vulnpy` web server with Contrast enabled using Docker:

1. Copy a `contrast_security.yaml` configuration file into the `vulnpy` root directory
2. Build the image with `docker build -t vulnpy .` from the `vulnpy` root
3. Run the container with `docker run --rm -it -p <port>:<port> -e PORT=<port> vulnpy`
	* Select a value for `<port>` to expose this port on your host machine
	* Optionally specify your framework with `-e FRAMEWORK=<some_framework>`
	* Framework options include django, falcon, flask, pyramid, and wsgi (default)
4. The webserver is now running on your selected port on the host machine

### Note on SSRF

By default, SSRF requests (requests made by the webserver to a third party) are mocked out, meaning
vulnpy will not send real requests when invoking SSRF endpoints. To disable this behavior and
enable vulnpy to send real network requests, set the VULNPY_REAL_SSRF_REQUESTS to any nonzero value.
The reason for this is simply to avoid accidentally overwhelming a third-party server when testing.

Vulnpy's sample web applications make use of this option.
