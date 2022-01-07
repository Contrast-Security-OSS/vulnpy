def ensure_binary(s, encoding="utf-8", errors="strict"):
    if isinstance(s, bytes):
        return s
    if isinstance(s, str):
        return s.encode(encoding, errors)
    raise TypeError(f"not expecting type '{type(s)}'")


def ensure_str(s, encoding="utf-8", errors="strict"):
    if type(s) is str:
        return s
    if isinstance(s, bytes):
        return s.decode(encoding, errors)
    elif not isinstance(s, (str, bytes)):
        raise TypeError(f"not expecting type '{type(s)}'")
