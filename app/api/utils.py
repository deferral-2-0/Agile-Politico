from flask import jsonify, make_response, abort
import json


def isint(val):
    """
    This function retunrs True if val
    is a number but false if it isnt
    """
    return isinstance(val, int)


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


def check_for_whitespace(data, items_to_check):
    """
    Check for whitespace on the data provided
    if the key of each itereable item is in the
    items_to_check list
    """
    for key, value in data.items():
        if key in items_to_check and not value.strip():
            abort(response_fn(400, "error",
                              '{} field cannot be left blank'.format(key)))

    return True


def check_for_ints(data, checklist):
    """
        this function checks if the items in the data selected
        from the checklist are integers.
    """
    return type_checks(isint, "field cannot be a non integer.", data, checklist)


def check_for_strings(data, checklist):
    """
    This function will check if values are strings right before
    calling the white space fn, this is because,
    we cannot call .strip on an int.
    type error issues
    """
    return type_checks(is_valid_string, "field cannot be a non string.", data, checklist)


def type_checks(pred, errormessage, data, checklist):
    """
        this function checks that values provided in the data args
        conform or pass the pred function test.
        if they dont pass, an error is thrown
    """
    for key, value in data.items():
        if key in checklist:
            if not pred(value):
                abort(response_fn(400, "error",
                                  '{} {}'.format(key, errormessage)))
    return True
