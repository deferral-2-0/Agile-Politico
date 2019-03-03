"""Tests for admin records"""
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db
from .base_test import BaseTestClass

import jwt
import os
KEY = os.getenv('SECRET_KEY')


class TestAdminEndpoint(BaseTestClass):
    def PostUser(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps({
                                    "username": "Tevyn",
                                    "firstname": "Tevin",
                                    "lastname": "Gach",
                                    "email": "tevinku@gmail.com",
                                    "phone": "0735464438",
                                    "othername": "Thuku",
                                    "password": "Tevin1995",
                                    "retypedpassword": "Tevin1995",
                                    "passportUrl": "http"
                                }),
                                content_type="application/json")

    def test_admin_setting_other_users_to_admin(self):
        self.PostUser()
        req = self.client.post("api/v2/authorize/2",
                               data=json.dumps({}),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        result = json.loads(req.data.decode("utf-8"))
        print(result)
        self.assertEqual(req.status_code, 200)

    def test_admin_setting_non_existent_user_to_admin(self):
        req = self.client.post("api/v2/authorize/200",
                               data=json.dumps({}),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        self.assertEqual(req.status_code, 404)

    def test_non_existent_admin_setting_non_existent_user_to_admin(self):
        usertoken = jwt.encode(
            {"email": "tevinkumr@gmail.com"}, KEY, algorithm='HS256')
        req = self.client.post("api/v2/authorize/200",
                               data=json.dumps({}),
                               headers={'x-access-token': usertoken},
                               content_type="application/json")
        self.assertEqual(req.status_code, 401)
