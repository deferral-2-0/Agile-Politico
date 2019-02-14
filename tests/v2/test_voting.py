"""Tests for voting endpoint """
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

        self.newoffice = {
            "type": "Governor",
            "name": "Governor Narok County"
        }
        self.newparty = {
            "name": "Party1",
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }

        self.properoffice = {
            "office": 1,
            "candidate": 1
        }

        self.missingcandidate = {
            "office": 1,
            "candidate": 100
        }

        self.missingOffice = {
            "office": 10,
            "candidate": 1
        }
        self.new_user_as_politician = {
            "username": "TevynPolitician",
            "firstname": "Tevin",
            "lastname": "Gach",
            "email": "tevinkupolitician@gmail.com",
            "phone": "0735464438",
            "othername": "Thuku",
            "password": "Tevin1995",
            "retypedpassword": "Tevin1995",
            "passportUrl": "http",
            "isPolitician": True
        }

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db()


class TestUserEndpoints(BaseTestClass):
    def NewUserAccountCreation(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps(self.new_user),
                                content_type="application/json")

    def CreatePoliticianUser(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps(self.new_user_as_politician),
                                content_type="application/json")

    def AdminCreateOffice(self):
        return self.client.post(
            "api/v2/offices",
            data=json.dumps(self.newoffice),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")

    def AdminCreateParty(self):
        return self.client.post(
            "api/v2/parties",
            data=json.dumps(self.newparty),
            headers={'x-access-token': self.admintoken},
            content_type="application/json")

    def AdminRegisterCandidate(self):
        return self.client.post("api/v2/offices/1/register",
                                data=json.dumps({
                                    "office": 1,
                                    "user": 2
                                }),
                                headers={'x-access-token': self.admintoken},
                                content_type="application/json")

    def RepeatProcedureBeforeVoting(self):
        self.NewUserAccountCreation()
        self.CreatePoliticianUser()
        self.AdminCreateOffice()
        self.AdminCreateParty()
        self.AdminRegisterCandidate()

    def test_user_voting_for_office(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps(self.properoffice), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_user_voting_twice(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        self.client.post("api/v2/votes", data=json.dumps(self.properoffice),
                         headers={'x-access-token': usertoken}, content_type="application/json")
        response = self.client.post("api/v2/votes", data=json.dumps({
            "office": 1,
            "candidate": 1}), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_vote_for_non_existent_office(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps(self.missingOffice), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_vote_for_non_existent_candidate(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps(self.missingcandidate), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_non_user_attempting_to_vote(self):
        self.RepeatProcedureBeforeVoting()
        response = self.client.post(
            "api/v2/votes", data=json.dumps(self.properoffice), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_unknown_user_attempting_to_vote(self):
        self.RepeatProcedureBeforeVoting()
        newusertoken = jwt.encode(
            {"email": "newuser@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps(self.properoffice), headers={'x-access-token': newusertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 401)
