"""Tests for password reset """
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

        self.correct_mail = {
            "email": "tevinku@gmail.com"
        }

        self.incorrect_mail = {
            "email": "wrongmail"
        }

        self.missing_mail = {
            "mail": "missing@gmail.com"  # note that mail == email
        }

        self.not_registered_user = {
            "email": "notregistered@gmail.com"
        }

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db(self.DB_URL)


class TestResetFunctionality(BaseTestClass):

    def test_reset_correct_mail_format(self):

        self.client.post("api/v2/auth/signup",
                         data=json.dumps(self.new_user),
                         content_type="application/json")
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps(self.correct_mail), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_wrongly_formatted_email(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps(self.incorrect_mail), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_missing_mail_in_payload(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps(self.missing_mail), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_reset_of_a_non_registered_user(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps(self.not_registered_user), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 404)
