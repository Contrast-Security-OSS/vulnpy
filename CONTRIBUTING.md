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

2. Add "do_triggername" function in the vulnerability file. **Note the
function definition must be prefixed with "do_".**

3. If your trigger requires installing a new python library, add it to setup.py in
`trigger_extras`.

4. Add a new file under templates/fragments/vulnname.frag.html OR use the existing
one to add a new fragment for the trigger. This step may be automated in the future.

5. Add a new `<li>` element to the menu bar in templates/fragments/base.html for this
vulnname.

6. Add a sample attack vector to vulnpy.trigger.DATA if you're adding a new category
of vulnerability.

7. Add tests under trigger/ and make sure to use `BaseTriggerTest`. Tests must be
added until - at a minimum - full test coverage is reached.
    * As part of this step you may need to update `DATA` if this is a new vulnerability.

8. Run an app with `make flask` (or other framework) to test this new vulnerability /
trigger(s):

    * No exceptions should appear when running `make flask`
    * Vulnpy home page should have a link to the vulnerability page in the navbar
    * Going to the vulnerability page shows the correct number of forms for each
      trigger function
    * Providing input to each of the trigger forms does not produce an exception


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
