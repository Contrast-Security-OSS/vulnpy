import pytest

from vulnpy.trigger import TRIGGER_MAP

VULN_NAMES = [x for x in TRIGGER_MAP if x != "util"]

ARGLIST = []
for vuln_name, trigger_names in TRIGGER_MAP.items():
    if not trigger_names:
        continue
    for trigger in trigger_names:
        ARGLIST.append((vuln_name, trigger))

parametrize_root = pytest.mark.parametrize("view_name", VULN_NAMES)
parametrize_triggers = pytest.mark.parametrize("view_name,trigger_name", ARGLIST)
