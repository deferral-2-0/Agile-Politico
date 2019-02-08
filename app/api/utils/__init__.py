"""
This functions can be reused as utlility functions accross the app and can be consumed
at any point by the different api endpoints
"""

from flask import jsonify, make_response


def is_valid_string(s):
    if s:
        return isinstance(s, str)
    else:
        return False


def is_valid_int(i):
    return isinstance(i, int)


def response_fn(status, key, message):
    dict = {
        "status": status
    }
    dict[key] = message
    return make_response(jsonify(dict), status)
