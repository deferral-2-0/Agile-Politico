# imports
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail
import jwt
from app.api import utils
import sys


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
        SELECT id, username, password, email, isAdmin, passportUrl, phone,
        firstname, lastname FROM users
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
                "email": item[3],
                "isAdmin": item[4],
            }
            try:
                d["passportUrl"] = item[5],
                d["phone"] = item[6],
                d["firstname"] = item[7],
                d["lastname"] = item[8]
            except IndexError:
                pass

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
        SELECT id, username, password, email, isAdmin FROM users"""
        return UserModel.format_user_list_to_record(db.select_data_from_db(select_all_users))

    @staticmethod
    def make_admin(userId):
        update_user = """
        UPDATE users SET isAdmin = True WHERE users.id = '{}'
        """.format(userId)

        db.queryData(update_user)

    @staticmethod
    def sendmail(email):
        """
            This function is responsible for sending an email 
            to the address provided as a parameter so that the user
            concerned can receive a notification via mail on 
            how to update their password.
        """
        try:
            username = UserModel.get_user_by_mail(email)[0][1]
        except:
            abort(utils.response_fn(404, "error",
                                    "You are not a registered user of the app"))
        token = jwt.encode({"email": email},
                           os.getenv('SECRET_KEY'), algorithm='HS256').decode('UTF-8')
        link = "https://tevinthuku.github.io/Politico/UI/setnewpassword.html?token={}".format(
            token)

        try:

            sg = sendgrid.SendGridAPIClient(
                apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("admin-noreply@politico.com")
            to_email = Email(email)
            subject = "Password reset instructions"
            content = Content(
                "text/plain",
                "Hey {} click this link to go and reset your password {}".format(username, link))
            mail = Mail(from_email, subject, to_email, content)
            sg.client.mail.send.post(request_body=mail.get())
        except:
            print('Unknown error detected:')
            # Info about unknown error that caused exception.
            a = sys.exc_info()
            print('    ', a)
            b = [str(p) for p in a]
            print('    ', b)
            abort(utils.response_fn(400, "error", "Something went wrongly here"))

    @staticmethod
    def update_password(email, newpassword):
        """
            This function updates the password of an account by setting the new
            password as provided in the parameters, the new password is first
            salted and then updated in the db
        """
        update_user = """
        UPDATE users SET password = '{}' WHERE users.email = '{}'
        """.format(generate_password_hash(str(newpassword)), email)

        db.queryData(update_user)
