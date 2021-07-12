from vulnpy.trigger.util import create_trigger_map, get_trigger  # noqa: F401

TRIGGER_MAP = create_trigger_map()


# This test data assumes that all triggers for the vulnerability accept the same
# user input. However, this isn't always true, as in the case of deserialization
# pickle and yaml. However, for test purposes, this is fine.
DATA = {
    "cmdi": "echo attack",
    "deserialization": "csubprocess\ncheck_output\n(S'ls'\ntR.",
    "hash": "hashme",
    "parameter_pollution": "",
    "pt": "../../etc/passwd",
    "rand": "seed",
    "redos": "anything",  # user input can be anything. The regex to be compared
    # against the REDOS regex may be be hardcoded.
    "sqli": "d', '4'),('e",
    "ssrf": "attacker.com",
    "unsafe_code_exec": "1 - 2",
    "xss": "attack",
    "xxe": "<root>attack</root>",
    "xpath": "./planet[name='Kepler']",
}
