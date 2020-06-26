# VulnPy

A library of purposely-vulnerable Python functions. These serve as a foundation for creating
insecure web applications, to be used for security testing and demonstration.

Do not use this library in a production environment!

## Installation

VulnPy contains both standalone functions and plug-and-play API extensions to various popular
Python web frameworks. To use vulnpy with your web framework, be sure to install this package with
the appropriate extra dependencies specified.

For example, for Flask, use the following command:

```
pip install 'git+git://github.com/Contrast-Security-OSS/vulnpy#egg=vulnpy[flask]'
```

Then, when setting up your application, register the vulnerable blueprint to your `Flask`
application object:

```py
from vulnpy.flask import vulnerable_blueprint

app = Flask(__name__)
app.register_blueprint(vulnerable_blueprint)
```
