from flask import jsonify, make_response


def is_valid_string(string_provided):
    """
    This function returns True
    if the item provided is a string
    and is not empty
    """
    if string_provided:
        return isinstance(string_provided, str)
    else:
        return False


def response_fn(status, key, message):
    """
        reuses the make_response and jsonify function
        so as not to forget to add the status after the
        jsonify call, which would return 200 after being
        left blank
    """
    dict = {
        "status": status
    }
    dict[key] = message
    return make_response(jsonify(dict), status)
