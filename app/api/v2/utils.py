import re
from flask import abort
from app.api.utils import response_fn
from app.api.v2.models.db import select_data_from_db


"""
This file includes all the necessary functions
required to interact with v2 of the api.

"""


def doPasswordsMatch(pass1, pass2):
    """
        this function checks if the passwords.
    """
    if(pass1 != pass2):
        abort(response_fn(400, "error", "passwords dont match"))
    return True


def is_phone_number_valid(phone):
    """
        This checks if a number phone number is valid
    """
    if not re.match('^[0-9]*$', phone):
        abort(response_fn(400, "Error", "Phone number should be integers only"))


def isEmailValid(email):
    """
        this function checks if the email is valid
        via regex
    """
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        abort(response_fn(400, "error", "email is invalid"))
    return True


def check_matching_items_in_db_table(params, table_name):
    """
        check if a value of key provided is 
        available in the database table
        if there's a duplicate then the test fails
    """
    for key, value in params.items():
        query = """
        SELECT {} from {} WHERE {}.{} = '{}'
        """.format(key, table_name, table_name, key, value)
        duplicated = select_data_from_db(query)
        print(duplicated)
        if duplicated:
            abort(response_fn(400, "error",
                              "Error. '{}' '{}' is already in use".format(key, value)))
