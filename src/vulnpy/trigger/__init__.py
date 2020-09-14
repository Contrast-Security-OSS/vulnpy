from importlib import import_module

TRIGGER_MAP = {
    "home": [],
    "cmdi": [
        "os-system",
        "subprocess-popen",
    ],
    "deserialization": [
        "pickle-load",
        "pickle-loads",
        "yaml-load",
        "yaml-load-all",
    ],
}


def get_trigger(name, trigger_name):
    """
    Find a function LIKE trigger_name in the module.

    :param name: str representing file name where trigger is located
    :param trigger_name: str
    :return: function
    """
    module_name = "vulnpy.trigger.{}".format(name)
    module = import_module(module_name)

    func_name = "do_{}".format(trigger_name.replace("-", "_"))

    try:
        return getattr(module, func_name)
    except AttributeError:
        print("Cannot find function {} in module {}", func_name, module.__name__)
        raise
