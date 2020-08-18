# Contributing to VulnPy

## Dev Environment Setup

We recommend entering a virtual environment and performing an editable install of this package with
all extra dependencies. Once in a virtualenv, run:

```sh
pip install -e '.[all]'
```

## Regenerating Templates

For maximum portability, the HTML returned by vulnpy endpoints does not require additional
rendering by a template engine. To achieve this with minimal code duplication, we generate all
HTML statically.

To modify existing templates, change or add HTML fragments in `vulnpy/templates/fragments`. Each
`*.frag.html` is spliced into the `base.html` skeleton. To regenerate templates, simply run:

```sh
make
```

Generated templates must be committed to this repository and will ship with the installed python
package for vulnpy.
