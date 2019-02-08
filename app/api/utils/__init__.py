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


def get_all_items(model, type):
    """
        returns different function calls based on the
        type provided.
        if none that matches , it defaults to zero.
        values are office | party
    """
    if(type == "office"):
        return model.get_all_offices()
    elif(type == "party"):
        return model.get_all_parties()
    return []


def get_specific_item(model, type, id):
    """
        This function takes a model, type (office | party) and 
        id of the item and returns the specific item from the 
        specified model, if a model does not have an item with the provided ID, 
        an empty list is returned.
    """
    if(type == "office"):
        return model.get_office(id)
    elif(type == "party"):
        return model.get_party(id)
    return []
