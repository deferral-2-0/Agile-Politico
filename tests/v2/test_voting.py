"""Tests for voting endpoint """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

from .base_test import BaseTestClass

import jwt
import os
KEY = os.getenv('SECRET_KEY')


class TestUserEndpoints(BaseTestClass):
    def NewUserAccountCreation(self):
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

    def CreatePoliticianUser(self):
        return self.client.post("api/v2/auth/signup",
                                data=json.dumps({
                                    "username": "TevynPolitician",
                                    "firstname": "Tevin",
                                    "lastname": "Gach",
                                    "email": "tevinkupolitician@gmail.com",
                                    "phone": "0735464438",
                                    "othername": "Thuku",
                                    "password": "Tevin1995",
                                    "retypedpassword": "Tevin1995",
                                    "passportUrl": "http"
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
                                    "user": 3
                                }),
                                headers={'x-access-token': self.ADMIN_TOKEN},
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
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 3
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_user_voting_twice(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        self.client.post("api/v2/votes", data=json.dumps({
            "office": 1,
            "candidate": 3
        }),
            headers={'x-access-token': usertoken}, content_type="application/json")
        response = self.client.post("api/v2/votes", data=json.dumps({
            "office": 1,
            "candidate": 3}), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_vote_for_non_existent_office(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 10,
                "candidate": 1
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_vote_for_non_existent_candidate(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 100
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_non_user_attempting_to_vote(self):
        self.RepeatProcedureBeforeVoting()
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 1
            }), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_unknown_user_attempting_to_vote(self):
        self.RepeatProcedureBeforeVoting()
        newusertoken = jwt.encode(
            {"email": "newuser@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 1
            }), headers={'x-access-token': newusertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_user_voting_for_office_with_invalid_types(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": "23",
                "candidate": "2"
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_user_voting_for_office_with_missing_info_on_candidate(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_getting_voting_results_of_an_office(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 3
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        res = self.client.get("api/v2/offices/1/result")
        self.assertEqual(res.status_code, 200)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [{
            "office": 1,
            "candidate": 3,
            "result": 1
        }])

    def test_getting_voting_results_before_any_vote(self):
        self.RepeatProcedureBeforeVoting()
        res = self.client.get("api/v2/offices/1/result")
        self.assertEqual(res.status_code, 200)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [])

    def test_getting_voting_pattern_for_a_user_after_a_vote(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')
        self.client.post(
            "api/v2/votes", data=json.dumps({
                "office": 1,
                "candidate": 3
            }), headers={'x-access-token': usertoken}, content_type="application/json")
        res = self.client.post("api/v2/votes/activity",
                               headers={'x-access-token': usertoken}, content_type="application/json", data=json.dumps({}))
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"],
                         [{'id': 1,
                           'info': 'You have already voted for TevynPolitician here',
                           'name': 'Governor Narok County',
                           'type': 'Governor'}])

    def test_getting_voting_pattern_for_a_user(self):
        self.RepeatProcedureBeforeVoting()
        usertoken = jwt.encode(
            {"email": "tevinku@gmail.com"}, KEY, algorithm='HS256')

        res = self.client.post("api/v2/votes/activity",
                               headers={'x-access-token': usertoken}, content_type="application/json", data=json.dumps({}))
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"],
                         [{'id': 1,
                           'info': [{'email': 'tevinkupolitician@gmail.com',
                                     'id': 3,
                                     'username': 'TevynPolitician'}],
                           'name': 'Governor Narok County',
                           'type': 'Governor'}])
