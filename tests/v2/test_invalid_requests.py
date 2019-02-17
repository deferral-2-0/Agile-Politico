"""Tests for offices endpoint """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

import jwt
import os
KEY = os.getenv('SECRET_KEY')
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


class BaseTestClass(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        init_db()

        self.admintoken = ADMIN_TOKEN

        self.newoffice = {
            "type": "Governor",
            "name": "Governor Narok County"
        }

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db()


class TestInvalidRequestsFunctionality(BaseTestClass):

    def test_admin_creating_office_with_invalid_content_type(self):
        res = self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': self.admintoken},
            content_type="application/text")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "content_type should be application/json")

    def test_admin_creating_office_with_missing_content_type(self):
        res = self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': self.admintoken},
            content_type="application/text")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "content_type should be application/json")

    def test_admin_create_office_with_invalid_json(self):
        res = self.client.post(
            "api/v2/offices",
            data="type: governor, name: governor of narok",
            headers={'x-access-token': self.admintoken},
            content_type="application/json")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "Data should be valid json")
