from flask import request, abort
from app.api.v2 import path_2

from app.api import utils
from app.api.v2 import utils as v2utils

from app.api.v2.models.users import UserModel
import psycopg2
from app.api.v2.utils import token_required, check_matching_items_in_db_table
from app.api.v2.utils import isUserAdmin

import requests
import json
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
        othername = data.get("othername", "")
        email = data["email"]
        phone = data["phone"]
        # doesnt have to fail because of absence of this value
        passportUrl = data.get("passportUrl", "")
        password = data["password"]
        retypedpassword = data["retypedpassword"]

    except:
        return abort(utils.response_fn(400, "error", 'Check your json keys. '
                                       'username, firstname, lastname,'
                                       'phone, email, password'))

    utils.check_for_strings(
        data, ["firstname", "lastname", "username", "othername", "passportUrl", "email", "phone"])

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
    token = jwt.encode({"email": email, "isAdmin": False},
                       KEY, algorithm='HS256')
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
    # check if both values are stirngs
    utils.check_for_strings(data, ["email", "password"])
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
        is_admin_prop = user[0][4]

        password = UserModel.check_if_password_n_hash_match(
            hashed_password, password)
        if not password:
            abort(utils.response_fn(400, "error",
                                    "The password is wrong, try again"))
        token = jwt.encode(
            {"email": email, "isAdmin": is_admin_prop}, KEY, algorithm='HS256')
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
    link = "https://tevpolitico.herokuapp.com/api/v2/auth/securereset"

    # send a request to the endpoint that will send the mail
    requests.post(
        link, data=json.dumps({"email": email}),
        headers={'Content-Type': 'application/json'}
    )
    return utils.response_fn(200, "data", [{
        "message": "Check your email for password reset link",
        "email": email
    }])

# send the email securely from server


@path_2.route("/auth/securereset", methods=["POST"])
def secure_reset():
    """
        this endpoint is to be requested 
        from the server only via the 
        /auth/reset view. Client browsers accessing this view will
        be forbidden and hence the mail will not be sent
        view https://sendgrid.com/docs/for-developers/sending-email/cors/
        for more details on the reasons this implementation is necessary
    """
    try:
        data = request.get_json()
        email = data["email"]
    except KeyError:
        abort(utils.response_fn(400, "error", "Should be email"))
    # check if email is valid
    v2utils.isEmailValid(email)
    UserModel.sendmail(email)
    return utils.response_fn(200, "data", [{
        "message": "Check your email for password reset link",
        "email": email
    }])


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


@path_2.route("/auth/newpassword", methods=["POST"])
def update_password():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

    except KeyError:
        abort(utils.response_fn(400, "error", "Should be email & password"))

    v2utils.check_password_format(password)

    user = UserModel.get_user_by_mail(email)
    if not user:
        abort(utils.response_fn(404, "error", "User does not exist"))

    UserModel.update_password(email, password)

    return utils.response_fn(200, "data", {
        "message": "Password reset successfully. Login with new password",
    })


@path_2.route('/users/<int:user_id>/edit', methods=['PATCH'])
@token_required
def bio_update(user, user_id):
    """ Updates user phone number """
    print(user)
    if user[0][1] == user_id:
        try:
            data = request.get_json()
            username = data['username']
            phone_num = data['phone_number']
            firstname = data['firstname']
            lastname = data['lastname']
            email = data['email']
            passportUrl = data['passporturl']
            othername = data['othername']

        except KeyError:
            abort(utils.response_fn(400, "error", "Missing Key"))

        v2utils.is_phone_number_valid(phone_num)

        utils.check_for_strings(
            data, ["username", "firstname", "lastname", "username", "othername", "passportUrl", "email", "phone"])

        utils.check_for_whitespace(
            data, ["username", "firstname", "lastname", "username", "email", "phone"])

        v2utils.isEmailValid(email)

        user = UserModel.get_user_by_id(user_id)

        if not user:
            abort(utils.response_fn(404, "error", "User does not exists"))

        UserModel.update_user_data(
            username, firstname, lastname, othername, phone_num, email, passportUrl, user_id)

        return utils.response_fn(200, "data", {
            "message": "You have successfuly updated your profile."
        })
    return utils.response_fn(401, "error", "You have to be the owner of the account to make changes.")
