"""Tests for books records"""
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
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL']
        init_db(self.DB_URL)

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

    # tear down tests

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db(self.DB_URL)


class TestUserEndpoints(BaseTestClass):
    def post_user(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps(self.new_user),
                                content_type="application/json")

    def test_user_creating_account_successfully(self):
        response = self.post_user()
        self.assertEqual(response.status_code, 201)
        print(response.data)
        result = json.loads(response.data.decode("utf-8"))

        self.assertEqual(result["status"], 201)

    def test_user_sign_up_with_missing_info(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(self.user_missing_info), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_for_mismatch_in_passwords(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.miss_match_user), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_for_duplicate_user(self):
        self.post_user()
        response = self.post_user()
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_for_wrong_email_format(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps(self.wrongmail_format), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)
