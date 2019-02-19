"""Tests candidates endpoint """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

from tests.v2.base_test import BaseTestClass

import jwt
import os
KEY = os.getenv('SECRET_KEY')


class TestUserEndpoints(BaseTestClass):
    def CreatePoliticianUser(self):
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
                                    "passportUrl": "http",
                                    "isPolitician": True
                                }),
                                content_type="application/json")

    def AdminCreateOffice(self):
        return self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")

    def AdminCreateParty(self):
        return self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": "Party1",
                "hqAddress": "Nairobi",
                "logoUrl": ""
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")

    def AdminRegisterCandidate(self):
        return self.client.post("api/v2/offices/1/register",
                                data=json.dumps({
                                    "office": 1,
                                    "user": 2
                                }),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")

    def test_admin_register_politician_candidate(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        res = self.AdminRegisterCandidate()
        self.assertEqual(res.status_code, 201)

    def test_admin_register_politician_candidate_twice(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        self.AdminRegisterCandidate()
        res = self.AdminRegisterCandidate()
        self.assertEqual(res.status_code, 400)

    def test_admin_register_politician_candidate_with_missing_params(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        res = self.client.post("api/v2/offices/1/register",
                               data=json.dumps({
                               }),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_admin_register_politician_in_non_existent_office(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        res = self.client.post("api/v2/offices/12/register",
                               data=json.dumps({
                                   "user": 2
                               }),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_admin_register_non_existent_user_to_office(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        res = self.client.post("api/v2/offices/12/register",
                               data=json.dumps({
                                   "user": 20
                               }),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_unauthorizedUser_registering_user_to_office(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        res = self.client.post("api/v2/offices/1/register",
                               data=json.dumps({
                                   "user": 20
                               }),
                               headers={'x-access-token': usertoken},
                               content_type="application/json")
        self.assertEqual(res.status_code, 401)

    def test_register_candidate_with_non_int_params(self):
        self.CreatePoliticianUser()  # 2
        self.AdminCreateParty()  # 1
        self.AdminCreateOffice()  # 1
        res = self.client.post("api/v2/offices/1/register",
                               data=json.dumps({
                                   "office": 1,
                                   "user": ""
                               }),
                               headers={'x-access-token': self.ADMIN_TOKEN},
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)
