import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md")) as f:
        README = f.read()
except IOError:
    README = ""

django_extras = ["Django"]
falcon_extras = ["falcon"]
flask_extras = ["Flask"]
pyramid_extras = ["pyramid"]
testing_extras = ["WebTest"]
all_extras = (
    django_extras + falcon_extras + flask_extras + pyramid_extras + testing_extras
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
    author_email="python@contrastsecurity.onmicrosoft.com",
    url="https://github.com/Contrast-Security-OSS/vulnpy",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
    extras_require={
        "all": all_extras,
        "django": django_extras,
        "falcon": falcon_extras,
        "flask": flask_extras,
        "pyramid": pyramid_extras,
    },
)
