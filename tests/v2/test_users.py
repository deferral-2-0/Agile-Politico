"""Tests for users records"""
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db


class BaseTestClass(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = app("testing")
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        init_db()

        self.new_user = {
            "username": "Tevyn",
            "firstname": "Tevin",
            "lastname": "Gach",
            "email": "tevinku@gmail.com",
            "phone": "0735464438",
            "othername": "Thuku",
            "password": "Tevin1995",
            "retypedpassword": "Tevin1995",
            "passportUrl": "http",
            "isPolitician": False
        }

        self.user_missing_info = {
            "username": "Missing",
            "firstname": "miss",
            "lastname": "ing"
        }

        self.miss_match_user = {
            "username": "Missmatch",
            "firstname": "MissmatchTom",
            "lastname": "Kensington",
            "email": "mismatchytom@gmail.com",
            "phone": "0735464438",
            "othername": "",
            "password": "Tom1997",
            "retypedpassword": "Tom1996",
            "passportUrl": "",
            "isPolitician": True
        }

        self.wrongmail_format = {
            "username": "Missmatch",
            "firstname": "MissmatchTom",
            "lastname": "Kensington",
            "email": "mismatchyto.com",
            "phone": "0735464438",
            "othername": "timberman",
            "password": "Tom1997",
            "retypedpassword": "Tom1997",
            "passportUrl": "",
            "isPolitician": True
        }

        self.new_wrong_number_format = {
            "username": "Tevyn",
            "firstname": "Tevin",
            "lastname": "Gach",
            "email": "tevinku@gmail.com",
            "phone": "hellonumber",
            "othername": "Thuku",
            "password": "Tevin1995",
            "retypedpassword": "Tevin1995",
            "passportUrl": "http",
            "isPolitician": False
        }

        self.login_new_user = {
            "email": "tevinku@gmail.com",
            "password": "Tevin1995"
        }

        self.login_new_user_with_wrong_password = {
            "email": "tevinku@gmail.com",
            "password": "Tevin1996"
        }

        self.adminlogin = {
            "email": "tevinthuku@gmail.com",
            "password": "BootcampWeek1"
        }

        self.poor_email_login = {
            "email": "tevinf",
            "password": "boomm"
        }

        self.missing_password_login = {
            "email": "youtube@gmail.com"
        }
        self.unknown_account = {
            "email": "trevork@gmail.com",
            "password": "Auth1234"
        }

        self.createaccountEmptyField = {
            "username": "",
            "firstname": "Tevin",
            "lastname": "Gach",
            "email": "tevinku@gmail.com",
            "phone": "0735464438",
            "othername": "Thuku",
            "password": "Tevin1995",
            "retypedpassword": "Tevin1995",
            "passportUrl": "http",
            "isPolitician": False
        }

        self.login_new_user_blankpassword = {
            "email": "tevinku@gmail.com",
            "password": ""
        }

    # tear down tests

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db()


class TestUserEndpoints(BaseTestClass):
    def PostUser(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps(self.new_user),
                                content_type="application/json")

    def test_user_creating_account_successfully(self):
        response = self.PostUser()
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 201)

    def test_user_creating_account_with_blank_field(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(
                                        self.createaccountEmptyField),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_sign_up_with_missing_info(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_missing_info), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_mismatch_in_passwords(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.miss_match_user), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_duplicate_user(self):
        self.PostUser()
        response = self.PostUser()
        self.assertEqual(response.status_code, 409)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 409)

    def test_user_sign_up_with_wrong_email_format(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.wrongmail_format), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_wrong_number_format(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.new_wrong_number_format), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    # login functionality

    def test_successfull_admin_login(self):
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps(self.adminlogin), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_successfull_user_login(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps(self.login_new_user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_login_with_bad_mail_format(self):
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            self.poor_email_login), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_login_with_present_but_blank_field(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps(self.login_new_user_blankpassword), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_login_with_missing_password_field(self):
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            self.missing_password_login), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_login_with_unknown_account(self):  # account not found
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            self.unknown_account), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 404)

    def test_with_wrong_password(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps(self.login_new_user_with_wrong_password), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_create_account_with_int_params(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": 12,
                                   "firstname": "Tevin",
                                   "lastname": "Gach",
                                   "email": "tevinku@gmail.com",
                                   "phone": "0735464438",
                                   "othername": "Thuku",
                                   "password": "Tevin1995",
                                   "retypedpassword": "Tevin1995",
                                   "passportUrl": "http",
                                   "isPolitician": False
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)
