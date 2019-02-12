# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class UserModel:
    """
    The v2 user model.
    """

    def __init__(self, username, email, password,
                 firstname, lastname, phone, passportUrl, isPolitician, othername):
        """
            Constructor of the user class
            New user objects are created with this method
        """
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.phone = phone
        self.password = self.encrypt_password_on_signup(password)
        self.passportUrl = passportUrl
        self.isPolitician = isPolitician
        self.othername = othername

    def save_user(self):
        """
        Add a new user to the users table
        """
        save_user_query = """
        INSERT INTO users(username, firstname, lastname, phone, email, password, passportUrl, isPolitician, othername, isAdmin) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname, self.phone, self.email, self.password, self.passportUrl, self.isPolitician, self.othername, False)

        db.query_data_from_db(save_user_query)

    def encrypt_password_on_signup(self, password):
        """
            hash password on sign up
        """
        hashed_password = generate_password_hash(str(password))
        return hashed_password
