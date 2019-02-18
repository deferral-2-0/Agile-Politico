"""Tests for offices endpoint """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

from .base_test import BaseTestClass
import jwt
import os
KEY = os.getenv('SECRET_KEY')
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


class TestInvalidRequestsFunctionality(BaseTestClass):

    def test_admin_creating_office_with_invalid_content_type(self):
        res = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
            }),
            headers={'x-access-token': ADMIN_TOKEN},
            content_type="application/text")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "content_type should be application/json")

    def test_admin_creating_office_with_missing_content_type(self):
        res = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
            }),
            headers={'x-access-token': ADMIN_TOKEN},
            content_type="application/text")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "content_type should be application/json")

    def test_admin_create_office_with_invalid_json(self):
        res = self.client.post(
            "api/v2/offices",
            data="type: governor, name: governor of narok",
            headers={'x-access-token': ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["error"],
                         "Data should be valid json")
