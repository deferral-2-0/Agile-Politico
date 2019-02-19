"""Tests for password reset """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

from .base_test import BaseTestClass


class TestResetFunctionality(BaseTestClass):

    def test_reset_correct_mail_format(self):

        self.client.post("api/v2/auth/signup",
                         data=json.dumps({
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
                         }),
                         content_type="application/json")
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps({
                                        "email": "tevinku@gmail.com"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_wrongly_formatted_email(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps({
                                        "email": "wrongmail"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_missing_mail_in_payload(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps({
                                        "mail": "missing@gmail.com"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_reset_of_a_non_registered_user(self):
        response = self.client.post("api/v2/auth/reset",
                                    data=json.dumps({
                                        "email": "notregistered@gmail.com"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 404)
