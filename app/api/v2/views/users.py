from flask import request
from app.api.v2 import path_2

from app.api import utils
from app.api.v2 import utils as v2utils

from app.api.v2.models.users import UserModel


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
        isPolitician = data.get("isPolitician", False)

    except:
        return utils.response_fn(400, "error", 'Check your json keys. '
                                 'username, firstname, lastname, othername ,phone, email, password, passportUrl')

    # check the passwords.
    v2utils.doPasswordsMatch(password, retypedpassword)
    # check the email provided
    v2utils.isEmailValid(email)

    v2utils.check_matching_items_in_db_table({"username": username}, "users")
    v2utils.check_matching_items_in_db_table({"email": email}, "users")

    newuser = UserModel(username, email, password, firstname,
                        lastname, phone, passportUrl, isPolitician, othername)
    newuser.save_user()

    return utils.response_fn(201, "data", [{
        "user": {
            "email": newuser.email,
            "username": newuser.username
        },
        "token": newuser.password
    }])
