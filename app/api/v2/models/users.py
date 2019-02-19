# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class UserModel:
    """
    The v2 user model.
    """

    def __init__(self, username, email, password,
                 firstname, lastname, phone, passportUrl, othername):
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
        self.othername = othername

    def save_user(self):
        """
        Add a new user to the users table
        """
        save_user_query = """
        INSERT INTO users(username,
        firstname, lastname, phone, email,
        password, passportUrl, isPolitician, othername, isAdmin) VALUES(
            '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
        )""".format(self.username, self.firstname, self.lastname,
                    self.phone, self.email, self.password,
                    self.passportUrl, False,
                    self.othername, False)

        db.queryData(save_user_query)

    @staticmethod
    def get_user(mechanism="email", value=""):
        """
            this method helps in reusing whether we want
            to check the user by ID or by email or username.
        """
        select_user_by_email = """
        SELECT id, username, password, email FROM users
        WHERE users.{} = '{}'""".format(mechanism, value)

        return db.select_data_from_db(select_user_by_email)

    def encrypt_password_on_signup(self, password):
        """
            hash password on sign up
        """
        hashed_password = generate_password_hash(str(password))
        return hashed_password

    @staticmethod
    def get_user_by_mail(email):
        return UserModel.get_user(mechanism="email", value=email)

    @staticmethod
    def get_user_by_id(id):
        """
            retrieve a user based on the ID.
            provided in the arguments.
        """
        return UserModel.get_user(mechanism="id", value=id)

    @staticmethod
    def format_user_list_to_record(iterable):
        results = []
        for item in iterable:
            d = {
                "id": item[0],
                "username": item[1],
                "email": item[2]
            }
            results.append(d)
        return results

    @staticmethod
    def get_user_by_id_formatted(id):
        """
            returns a record of a user
        """
        data = UserModel.get_user_by_id(id)

        return UserModel.format_user_list_to_record(data)[0]

    @staticmethod
    def check_if_password_n_hash_match(password_hash, password):
        return check_password_hash(password_hash, str(password))

    @staticmethod
    def get_all_users():
        select_all_users = """
        SELECT id, username, email FROM users"""
        return UserModel.format_user_list_to_record(db.select_data_from_db(select_all_users))
