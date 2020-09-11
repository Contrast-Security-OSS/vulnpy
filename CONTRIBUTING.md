# Contributing to VulnPy

## Dev Environment Setup

We recommend entering a virtual environment and performing an editable install of this package with
all extra dependencies. Once in a virtualenv, run:

```sh
pip install -e '.[all]'
```

## Adding New Triggers

Vulnpy is able to automatically generate view definitions for all supported 
frameworks when a new trigger is added. To add a new trigger:

1. Add a new file under trigger/ if the vulnerability you are adding doesn't have one
 already
 
2. Add "do_vulnname_triggername" function in the vulnerability file. Note the 
function definition must be prefixed with "do_".

3. Add trigger name to TRIGGER_MAP. Note that at this time Vulnpy makes some 
assumptions about the 
trigger name strings so you may need to modify this string to use underscores or dashes.

4. Add a new file under templates/fragments/vulnname.frag.html OR use the existing 
one to add a new fragment for the trigger. This step may be automated in the future.

5. Add tests under trigger/ and for each of the frameworks to call the new trigger.


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
