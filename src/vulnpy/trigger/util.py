import glob
import inspect
from importlib import import_module
from os.path import dirname, basename, isfile, join


def _get_trigger_files():
    """
    Find the file names under /trigger.

    :return: list of str partial file names, ie ['cmdi', 'deserialization']
    """
    all_files = glob.glob(join(dirname(__file__), "*.py"))
    trigger_files = [
        basename(f)[:-3]
        for f in all_files
        if isfile(f) and not f.endswith("__init__.py")
    ]

    return trigger_files


def _get_trigger_module(name):
    module_name = "vulnpy.trigger.{}".format(name)
    return import_module(module_name)


def create_trigger_map():
    map = {"home": []}

    trigger_files = _get_trigger_files()

    for vuln_name in trigger_files:
        map.setdefault(vuln_name, [])

        module = _get_trigger_module(vuln_name)

        for obj_name, _ in inspect.getmembers(module):
            if obj_name.startswith("do"):
                trigger_name = obj_name.replace("do_", "").replace("_", "-")
                map[vuln_name].append(trigger_name)

    return map


def get_trigger(name, trigger_name):
    """
    Find a function LIKE trigger_name in the module.

    :param name: str representing file name where trigger is located
    :param trigger_name: str
    :return: function
    """
    module = _get_trigger_module(name)

    func_name = "do_{}".format(trigger_name.replace("-", "_"))

    try:
        return getattr(module, func_name)
    except AttributeError:
        print("Cannot find function {} in module {}", func_name, module.__name__)
        raise
