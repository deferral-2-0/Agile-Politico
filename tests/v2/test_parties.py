"""Tests for password reset """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

import jwt
import os
KEY = os.getenv('SECRET_KEY')


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

        self.login_new_user = {
            "email": "tevinku@gmail.com",
            "password": "Tevin1995"
        }

        self.newparty = {
            "name": "Party1",
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }

        self.missinginfoparty = {
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }

        self.admintoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRldmludGh1a3VAZ21haWwuY29tIn0.Nehevl-RbT5FFF484k1fuW9DV7u5ZqrgiPqAe7igpwA"

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db(self.DB_URL)


class TestPartiesFunctionality(BaseTestClass):
    def CreateUser(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps(self.new_user),
                                content_type="application/json")

    def test_fetching_all_parties(self):
        response = self.client.get("api/v2/parties",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_posting_party_as_admin(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 201)

    def test_posting_party_anonymously(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_ordinary_user_attempting_to_create_a_party(self):
        self.CreateUser()
        userdata = self.client.post(
            "api/v2/auth/signin", data=json.dumps(self.login_new_user), content_type="application/json")
        usertoken = json.loads(userdata.data.decode("utf-8"))["data"]["token"]
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            headers={'x-access-token': usertoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_admin_post_party_with_missing_fields(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps(self.missinginfoparty),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_unidentified_user_creating_party(self):
        mocktoken = jwt.encode(
            {"email": "ninja@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            headers={'x-access-token': mocktoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_view_list_after_insert(self):
        self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")
        response = self.client.get("api/v2/parties",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["data"], [{
            "id": 1,
            "name": "Party1",
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }])
