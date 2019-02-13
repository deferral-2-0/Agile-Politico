"""Tests for offices endpoint """
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
        self.app.config['TESTING'] = True
        init_db()

        self.admintoken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRldmludGh1a3VAZ21haWwuY29tIn0.Nehevl-RbT5FFF484k1fuW9DV7u5ZqrgiPqAe7igpwA"
        self.newoffice = {
            "type": "Governor",
            "name": "Governor Narok County"
        }

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db()


class TestOfficesFunctionality(BaseTestClass):

    def AdminPostOffice(self):
        return self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")

    def test_admin_creating_office(self):
        res = self.AdminPostOffice()
        self.assertEqual(res.status_code, 201)

    def test_admin_creating_office_with_missing_fields(self):
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "name": "Office 2"
            }),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_office_with_bad_token(self):
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': "hsankerereewe3424"},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_unkown_user_create_office(self):
        usertoken = jwt.encode(
            {"email": "johndoe@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': usertoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_view_all_offices(self):
        res = self.client.get("api/v2/offices")
        self.assertEqual(res.status_code, 200)

    def test_view_offices_after_insert(self):
        self.AdminPostOffice()
        res = self.client.get("api/v2/offices")
        self.assertEqual(res.status_code, 200)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [{
            "id": 1,
            "name": "Governor Narok County",
            "type": "Governor"
        }])
