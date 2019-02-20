import re
from flask import abort, request
from functools import wraps
from app.api.utils import response_fn
from app.api.v2.models.db import select_data_from_db
import jwt
import os
KEY = os.getenv('SECRET_KEY')

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
    check_password_format(pass1)


def check_password_format(password):
    '''
     Does password meet expectations
     of passwords that need to be saved
    '''
    # check to confirm the password is of required length
    if len(password) < 5 or len(password) > 20:
        abort(response_fn(400, "error",
                          "Password should not be less than 8 characters or exceed 20"))

    smallreg = re.search("[a-z]", password)
    largereg = re.search("[A-Z]", password)
    numreg = re.search("[0-9]", password)
    if not smallreg or not largereg or not numreg:
        abort(response_fn(400,
                          "error",
                          "Password should contain at least 1 number, 1 small letter and 1 Capital letter"))


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
        if duplicated:
            abort(response_fn(409, "error",
                              "Error. '{}' '{}' is already in use".format(key, value)))


def token_required(f):
    """
        This higher order function checks for token in the request
        Headers
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return response_fn(401, "error", "Token is missing")
        try:
            data = jwt.decode(token, KEY, algorithms='HS256')
            query = """
            SELECT email, id, isAdmin FROM users
            WHERE users.email = '{}'""".format(data['email'])

            user = select_data_from_db(query)

        except:
            return response_fn(401, "error", "Token is expired or invalid")

        return f(user, *args, **kwargs)
    return decorated


def isUserAdmin(adminProp):
    """
        This function checks if the user is an admin.
    """
    if not adminProp:
        abort(response_fn(401, "error", "You are not an admin"))

# SELECT candidate, COUNT(candidate) AS result, office FROM votes WHERE votes.office = 1 GROUP BY candidate, office;
# SELECT candidate, COUNT(candidate) AS result, office FROM votes GROUP BY candidate, office;
