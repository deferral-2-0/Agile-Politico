"""Tests for password reset """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db

from .base_test import BaseTestClass
import jwt
import os
KEY = os.getenv('SECRET_KEY')


class TestPartiesFunctionality(BaseTestClass):
    def CreateUser(self):
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
                                    "isPolitician": False
                                }),
                                content_type="application/json")

    def AdminPostParty(self):
        return self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": "Party1",
                "hqAddress": "Nairobi",
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")

    def test_fetching_all_parties(self):
        response = self.client.get("api/v2/parties",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_posting_party_as_admin(self):
        response = self.AdminPostParty()
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 201)

    def test_posting_party_as_admin_with_missingfields(self):
        res = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                            "name": "Party1",
                            "hqAddress": "",
                            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")

        self.assertEqual(res.status_code, 400)

    def test_posting_party_anonymously(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": "Party1",
                "hqAddress": "Nairobi",
                "logoUrl": ""
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_ordinary_user_attempting_to_create_a_party(self):
        self.CreateUser()
        userdata = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "tevinku@gmail.com",
                "password": "Tevin1995"
            }), content_type="application/json")
        usertoken = json.loads(userdata.data.decode("utf-8"))["data"]["token"]
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": "Party1",
                "hqAddress": "Nairobi"
            }),
            headers={'x-access-token': usertoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_admin_post_party_with_missing_fields(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "hqAddress": "Nairobi",
                "logoUrl": ""
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_admin_post_party_with_int_types(self):
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": 12,
                "hqAddress": "Int name",
                "logoUrl": "logoUrl"
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_unidentified_user_creating_party(self):
        mocktoken = jwt.encode(
            {"email": "ninja@gmail.com"}, KEY, algorithm='HS256')
        response = self.client.post(
            "api/v2/parties",
            data=json.dumps({
                "name": "Party1",
                "hqAddress": "Nairobi",
                "logoUrl": ""
            }),
            headers={'x-access-token': mocktoken},
            content_type="application/json")
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 401)

    def test_view_list_after_insert(self):
        self.AdminPostParty()
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

    def test_getting_specific_party(self):
        self.AdminPostParty()
        res = self.client.get("api/v2/parties/1")
        self.assertEqual(res.status_code, 200)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [{
            "id": 1,
            "name": "Party1",
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }])

    def test_getting_missing_party(self):
        res = self.client.get("api/v2/parties/3")
        self.assertEqual(res.status_code, 404)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["status"], 404)

    def test_admin_updating_existing_party(self):
        self.AdminPostParty()
        res = self.client.patch("api/v2/parties/1/name",
                                data=json.dumps({"name": "Party A"}),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")
        self.assertEqual(res.status_code, 200)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["data"], [{
            "id": 1,
            "name": "Party A"
        }])

    def test_admin_updating_existing_party_with_blank_name(self):
        self.AdminPostParty()
        res = self.client.patch("api/v2/parties/1/name",
                                data=json.dumps({"name": ""}),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_admin_updating_existing_party_with_int_name(self):
        self.AdminPostParty()
        res = self.client.patch("api/v2/parties/1/name",
                                data=json.dumps({"name": 12}),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_getting_all_parties_after_deletion(self):
        self.AdminPostParty()
        self.client.patch("api/v2/parties/1/name",
                          data=json.dumps({"name": "Party A"}),
                          headers={'x-access-token': self.ADMIN_TOKEN},
                          content_type="application/json")
        response = self.client.get("api/v2/parties",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["data"], [{
            "id": 1,
            "name": "Party A",
            "hqAddress": "Nairobi",
            "logoUrl": ""
        }])

    def test_admin_updating_non_existent_party(self):
        res = self.client.patch("api/v2/parties/20/name",
                                data=json.dumps({"name": "Party 20 num"}),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")
        self.assertEqual(res.status_code, 404)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["status"], 404)

    def test_admin_updating_with_no_params_provided(self):
        self.AdminPostParty()
        res = self.client.patch("api/v2/parties/1/name",
                                data=json.dumps(
                                    {"newname": "Missing new name"}),
                                headers={'x-access-token': self.ADMIN_TOKEN},
                                content_type="application/json")
        self.assertEqual(res.status_code, 400)
        dataresponse = json.loads(res.data.decode("utf-8"))
        self.assertEqual(dataresponse["status"], 400)

    def test_ordinary_user_updating_party(self):
        self.AdminPostParty()
        ordinaryuser = jwt.encode(
            {"email": "johndoe@gmail.com"}, KEY, algorithm='HS256')
        res = self.client.patch("api/v2/parties/1/name",
                                data=json.dumps({"name": "Party 20 num"}),
                                headers={'x-access-token': ordinaryuser},
                                content_type="application/json")
        self.assertEqual(res.status_code, 401)

    def test_admin_deleting_party(self):
        self.AdminPostParty()
        res = self.client.delete(
            "/api/v2/parties/{}".format(1),
            content_type="application/json",
            headers={'x-access-token': self.ADMIN_TOKEN}
        )
        self.assertEqual(res.status_code, 200)

    def test_admin_deleting_non_existing_party(self):
        self.AdminPostParty()
        res = self.client.delete(
            "/api/v2/parties/{}".format(100),
            content_type="application/json",
            headers={"x-access-token": self.ADMIN_TOKEN}
        )
        self.assertEqual(res.status_code, 404)

    def test_ordinary_user_deleting_party(self):
        self.AdminPostParty()
        ordinaryuser = jwt.encode(
            {"email": "johndoe@gmail.com"}, KEY, algorithm='HS256')
        res = self.client.delete(
            "/api/v2/parties/{}".format(1),
            content_type="application/json",
            headers={"x-access-token": ordinaryuser}
        )
        self.assertEqual(res.status_code, 401)
