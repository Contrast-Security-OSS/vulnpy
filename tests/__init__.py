import pytest

from vulnpy.trigger import TRIGGER_MAP


def _make_trigger_list():
    arglist = []
    for vuln_name, trigger_names in TRIGGER_MAP.items():
        if not trigger_names:
            continue
        for trigger in trigger_names:
            arglist.append((vuln_name, trigger))

    return arglist


def _make_view_paths():
    view_paths = []

    for vuln_name in TRIGGER_MAP:
        if vuln_name == "util":
            continue

        if vuln_name == "home":
            path = "/vulnpy"
        else:
            path = "/vulnpy/{}".format(vuln_name)

        view_paths.append(path)

    return view_paths


parametrize_root = pytest.mark.parametrize("view_path", _make_view_paths())
parametrize_triggers = pytest.mark.parametrize(
    "view_name,trigger_name", _make_trigger_list()
)
