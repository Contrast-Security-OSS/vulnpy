from vulnpy.trigger.util import create_trigger_map, get_trigger  # noqa: F401

TRIGGER_MAP = create_trigger_map()

DATA = {
    "cmdi": "echo attack",
    "deserialization": "csubprocess\ncheck_output\n(S'ls'\ntR.",  # TODO yaml data
    "unsafe_code_exec": "1 + 2",
    "xxe": "<root>attack</root>",
}
