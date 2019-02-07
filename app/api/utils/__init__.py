def is_valid_string(s):
    if s:
        return isinstance(s, str)
    else:
        return False


def is_valid_int(i):
    return isinstance(i, int)
