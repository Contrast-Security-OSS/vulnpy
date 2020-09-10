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


def get_trigger(module, trigger_name):
    """
    Find a function LIKE trigger_name in the module.

    :param module: Python module
    :param trigger_name: str
    :return: function
    """
    func_name = "do_{}".format(trigger_name.replace("-", "_"))

    try:
        return getattr(module, func_name)
    except AttributeError:
        return
