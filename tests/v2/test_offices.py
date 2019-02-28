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


class TestOfficesFunctionality(BaseTestClass):

    def AdminPostOffice(self):
        return self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
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

    def test_admin_creating_office(self):
        res = self.AdminPostOffice()
        self.assertEqual(res.status_code, 201)

    def test_admin_creating_office_with_missing_fields(self):
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "name": "Office 2"
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_office_with_bad_token(self):
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
            }),
            headers={'x-access-token': "hsankerereewe3424"},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_unkown_user_create_office(self):
        usertoken = jwt.encode(
            {"email": "johndoe@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "type": "Governor",
                "name": "Governor Narok County"
            }),
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

    def test_getting_specific_party(self):
        self.AdminPostOffice()
        res = self.client.get("api/v2/offices/1")
        self.assertEqual(res.status_code, 200)

    def test_getting_undefined_office(self):
        res = self.client.get("api/v2/offices/100")
        self.assertEqual(res.status_code, 404)

    def test_whitespaces_in_office_creation(self):
        res = self.client.post(
            "api/v2/offices",
            data=json.dumps({
                "name": "Senator Office",
                "type": ""
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_get_candidates_in_particular_office(self):
        req = self.client.get("api/v2/offices/1/candidates",
                              content_type="application/json")
        self.assertEqual(req.status_code, 200)
        dataresponse = json.loads(req.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [])

    def test_getting_candidate_after_registering_candidate_to_an_office(self):
        self.CreatePoliticianUser()
        self.AdminPostOffice()
        self.AdminRegisterCandidate()
        req = self.client.get("api/v2/offices/1/candidates",
                              content_type="application/json")
        self.assertEqual(req.status_code, 200)
        dataresponse = json.loads(req.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [
                         {'email': 'tevinku@gmail.com', 'id': 2, 'username': 'Tevyn'}])

    def test_getting_meta_info_after_registering_candidate_to_office_and_voting(self):
        self.CreatePoliticianUser()
        self.AdminPostOffice()
        self.AdminRegisterCandidate()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 2
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        req = self.client.get("api/v2/offices/metainfo",
                              content_type="application/json")
        self.assertEqual(req.status_code, 200)
        dataresponse = json.loads(req.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"],
                         [{'candidates': [{'email': 'tevinku@gmail.com',
                                           'result': 1,
                                           'username': 'Tevyn'}],
                           'id': 1,
                           'name': 'Governor Narok County',
                           'type': 'Governor'}])

    def test_getting_meta_info_after_registering_candidate_to_office(self):
        self.CreatePoliticianUser()
        self.AdminPostOffice()
        self.AdminRegisterCandidate()
        req = self.client.get("api/v2/offices/metainfo",
                              content_type="application/json")
        self.assertEqual(req.status_code, 200)
        dataresponse = json.loads(req.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"],
                         [{'candidates': [{'email': 'tevinku@gmail.com',
                                           'result': 0,
                                           'username': 'Tevyn'}],
                           'id': 1,
                           'name': 'Governor Narok County',
                           'type': 'Governor'}])
