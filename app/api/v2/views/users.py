from flask import request, abort
from app.api.v2 import path_2

from app.api import utils
from app.api.v2 import utils as v2utils

from app.api.v2.models.users import UserModel
import psycopg2
from app.api.v2.utils import token_required, check_matching_items_in_db_table
from app.api.v2.utils import isUserAdmin


import os
import jwt

KEY = os.getenv('SECRET_KEY')


@path_2.route("/auth/signup", methods=["POST"])
def signup():
    """
        Sign a user up
    """
    try:
        data = request.get_json()
        firstname = data['firstname']
        lastname = data['lastname']
        username = data["username"]
        othername = data.get("othername", "none")
        email = data["email"]
        phone = data["phone"]
        # doesnt have to fail because of absence of this value
        passportUrl = data.get("passportUrl", "")
        password = data["password"]
        retypedpassword = data["retypedpassword"]

    except:
        return abort(utils.response_fn(400, "error", 'Check your json keys. '
                                       'username, firstname, lastname, othername,'
                                       'phone, email, password, passportUrl'))

    utils.check_for_strings(
        data, ["firstname", "lastname", "username", "username", "email", "phone"])

    utils.check_for_whitespace(
        data, ["firstname", "lastname", "username", "email", "phone"])

    utils.check_for_bools(data, ["isAdmin", "isPolitician"])
    # check the passwords.
    v2utils.doPasswordsMatch(password, retypedpassword)
    # check the email provided
    v2utils.isEmailValid(email)
    # Check if phone number is valid
    v2utils.is_phone_number_valid(phone)

    v2utils.check_matching_items_in_db_table({"username": username}, "users")
    v2utils.check_matching_items_in_db_table({"email": email}, "users")

    newuser = UserModel(username=username, email=email, password=password, firstname=firstname,
                        lastname=lastname, phone=phone, passportUrl=passportUrl, othername=othername)
    newuser.save_user()
    token = jwt.encode({"email": email}, KEY, algorithm='HS256')
    return utils.response_fn(201, "data", [{
        "user": {
            "email": newuser.email,
            "username": newuser.username
        },
        "token": token.decode('UTF-8')
    }])


# login route
@path_2.route("/auth/signin", methods=['POST'])
def user_login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be email & password"))

    # check for the validity of the email
    v2utils.isEmailValid(email)
    # check for whitespaces.
    utils.check_for_whitespace(data, ["email", "password"])

    # try to get the record of the user by email.
    try:
        user = UserModel.get_user_by_mail(email)
        if not user:
            abort(utils.response_fn(404, "error", "User does not exist"))

        id = user[0][0]
        username = user[0][1]
        hashed_password = user[0][2]

        password = UserModel.check_if_password_n_hash_match(
            hashed_password, password)
        if not password:
            abort(utils.response_fn(400, "error",
                                    "The paswwsord is wrong, try again"))
        token = jwt.encode({"email": email}, KEY, algorithm='HS256')
        return utils.response_fn(200, "data", {
            "message": "Logged in successfully",
            "token": token.decode('UTF-8'),
            "user": {
                "id": id,
                "username": username
            }
        })
    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))


# password reset route
@path_2.route("/auth/reset", methods=["POST"])
def reset_password():
    try:
        data = request.get_json()
        email = data["email"]
    except KeyError:
        abort(utils.response_fn(400, "error", "Should be email"))

    # check if email is valid
    v2utils.isEmailValid(email)
    # if user doesn't exist dont send an email to them
    try:
        user = UserModel.get_user_by_mail(email)
        if not user:
            abort(utils.response_fn(404, "error",
                                    "User does not exist. Create an account first"))
        return utils.response_fn(200, "data", [{
            "message": "Check your email for password reset link",
            "email": email
        }])
    except psycopg2.DatabaseError as _error:
        abort(utils.response_fn(500, "error", "Server error"))

# getting list of all users


@path_2.route("/users", methods=["GET"])
def get_all_users():
    return utils.response_fn(200, "data", UserModel.get_all_users())


@path_2.route("/authorize/<int:user_id>", methods=["POST"])
@token_required
def authorize_user_to_admin(user, user_id):
    try:
        adminprop = user[0][2]
    except:
        return utils.response_fn(401, "error",
                                 "You don't have an account. Create One")

    isUserAdmin(adminprop)
    userToBeElevated = UserModel.get_user_by_id(user_id)

    if userToBeElevated:
        UserModel.make_admin(userToBeElevated[0][0])
        return utils.response_fn(200, "data", [{
            "message": "Admin has been set"
        }])
    return utils.response_fn(404, "message",
                             "The user you are trying to elevate is not registered")
