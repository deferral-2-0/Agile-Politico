"""Tests for users records"""
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db
from .base_test import BaseTestClass


class TestUserEndpoints(BaseTestClass):
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

    """ Candidate application details """
    def user_candidature_application(self):
        return self.client.post("api/v2/offices/apply",
                                data=json.dumps({
                                    "name":"linc lidanya",
                                    "email":"linclid@gmail.com",
                                    "position":"president"
                                }),
                                content_type="application/json")

    """ Test for candidature application """
    def test_apply_candidature(self):
        self.PostUser()
        self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "tevinku@gmail.com",
                "password": "Tevin1995"
            }), content_type="application/json")
        res=self.client.post("api/v2/offices/apply", data=json.dumps({
                "email":"linclid@gmail.com",
                "position":"president"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 201)

    def test_user_creating_account_successfully(self):
        response = self.PostUser()
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 201)

    def test_user_creating_account_with_blank_field(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(
                                        {
                                            "username": "",
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
        self.assertEqual(response.status_code, 400)

    def test_user_sign_up_with_missing_info(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps({
                                        "username": "Missing",
                                        "firstname": "miss",
                                        "lastname": "ing"
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_mismatch_in_passwords(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps({
                "username": "Missmatch",
                "firstname": "MissmatchTom",
                "lastname": "Kensington",
                "email": "mismatchytom@gmail.com",
                "phone": "0735464438",
                "othername": "",
                "password": "Tom1997",
                "retypedpassword": "Tom1996",
                "passportUrl": "",
                "isPolitician": True
            }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_duplicate_user(self):
        self.PostUser()
        response = self.PostUser()
        self.assertEqual(response.status_code, 409)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 409)

    def test_user_sign_up_with_wrong_email_format(self):
        response = self.client.post(
            "api/v2/auth/signup", data=json.dumps({
                "username": "Missmatch",
                "firstname": "MissmatchTom",
                "lastname": "Kensington",
                "email": "mismatchyto.com",
                "phone": "0735464438",
                "othername": "timberman",
                "password": "Tom1997",
                "retypedpassword": "Tom1997",
                "passportUrl": "",
                "isPolitician": True
            }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_sign_up_with_wrong_number_format(self):
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps({
                                        "username": "Tevyn",
                                        "firstname": "Tevin",
                                        "lastname": "Gach",
                                        "email": "tevinku@gmail.com",
                                        "phone": "hellonumber",
                                        "othername": "Thuku",
                                        "password": "Tevin1995",
                                        "retypedpassword": "Tevin1995",
                                        "passportUrl": "http",
                                        "isPolitician": False
                                    }), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    # login functionality

    def test_successfull_admin_login(self):
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "admindetails@gmail.com",
                "password": "BootcampWeek1"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_successfull_user_login(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "tevinku@gmail.com",
                "password": "Tevin1995"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)

    def test_login_with_bad_mail_format(self):
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            {
                "email": "tevinf",
                "password": "boomm"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_user_login_with_present_but_blank_field(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "tevinku@gmail.com",
                "password": ""
            }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_login_with_missing_password_field(self):
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            {
                "email": "youtube@gmail.com"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_login_with_unknown_account(self):  # account not found
        res = self.client.post("api/v2/auth/signin", data=json.dumps(
            {
                "email": "trevork@gmail.com",
                "password": "Auth1234"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 404)

    def test_with_wrong_password(self):
        self.PostUser()
        res = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "tevinku@gmail.com",
                "password": "Tevin1996"
            }), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_create_account_with_int_params(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": 12,
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
        self.assertEqual(res.status_code, 400)

    def test_non_bool_params(self):
        res = self.client.post("api/v2/auth/signup",
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
                                   "isPolitician": "dsdwe"
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_getting_users_list(self):
        res = self.client.get("api/v2/users")
        self.assertEqual(res.status_code, 200)

    def test_getting_list_of_users(self):
        res = self.client.get("api/v2/users")
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["data"], [
                         {'email': 'admindetails@gmail.com', 'id': 1, 'username': 'OriginalAdmin', 'isAdmin': True}])

    def test_password_without_number(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": "Tevyn",
                                   "firstname": "Tevin",
                                   "lastname": "Gach",
                                   "email": "tevinku@gmail.com",
                                   "phone": "0735464438",
                                   "othername": "Thuku",
                                   "password": "Tevint",
                                   "retypedpassword": "Tevint",
                                   "passportUrl": "http"
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_password_without_caps(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": "Tevyn",
                                   "firstname": "Tevin",
                                   "lastname": "Gach",
                                   "email": "tevinku@gmail.com",
                                   "phone": "0735464438",
                                   "othername": "Thuku",
                                   "password": "tevint",
                                   "retypedpassword": "tevint",
                                   "passportUrl": "http"
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_password_less_than_5(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": "Tevyn",
                                   "firstname": "Tevin",
                                   "lastname": "Gach",
                                   "email": "tevinku@gmail.com",
                                   "phone": "0735464438",
                                   "othername": "Thuku",
                                   "password": "tev",
                                   "retypedpassword": "tev",
                                   "passportUrl": "http"
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_password_all_caps(self):
        res = self.client.post("api/v2/auth/signup",
                               data=json.dumps({
                                   "username": "Tevyn",
                                   "firstname": "Tevin",
                                   "lastname": "Gach",
                                   "email": "tevinku@gmail.com",
                                   "phone": "0735464438",
                                   "othername": "Thuku",
                                   "password": "TEVINTHUKU",
                                   "retypedpassword": "TEVINTHUKU",
                                   "passportUrl": "http"
                               }),
                               content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_update_user_password(self):
        res = self.client.post("api/v2/auth/newpassword", data=json.dumps({
            "email": "admindetails@gmail.com",
            "password": "Tevinrocks1995"
        }), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        loginres = self.client.post(
            "api/v2/auth/signin", data=json.dumps({
                "email": "admindetails@gmail.com",
                "password": "Tevinrocks1995"
            }), content_type="application/json")

        self.assertEqual(loginres.status_code, 200)

    def test_updating_password_of_non_user(self):
        res = self.client.post("api/v2/auth/newpassword", data=json.dumps({
            "email": "tevothuku@gmail.com",
            "password": "Tevinrocks1995"
        }), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_updating_password_with_missing_password(self):
        res = self.client.post("api/v2/auth/newpassword", data=json.dumps({
            "email": "tevothuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_secure_endpoint_for_sending_emails(self):
        self.client.post("api/v2/auth/signup",
                         data=json.dumps({
                             "username": "Tevyn",
                             "firstname": "Tevin",
                             "lastname": "Gach",
                             "email": "tevinthuku@gmail.com",
                             "phone": "0735464438",
                             "othername": "Thuku",
                             "password": "Tevinrocks1995",
                             "retypedpassword": "Tevinrocks1995",
                             "passportUrl": "http"
                         }),
                         content_type="application/json")
        res = self.client.post("api/v2/auth/securereset", data=json.dumps({
            "email": "tevinthuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_secure_endpoint_for_sending_emails_with_no_email(self):
        res = self.client.post("api/v2/auth/securereset", data=json.dumps({
            "password": "tevothuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_secure_endpoint_for_sending_emails_with_invalid_email(self):
        res = self.client.post("api/v2/auth/securereset", data=json.dumps({
            "email": "tevotmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_secure_endpoint_for_sending_emails_with_non_existent_user(self):
        res = self.client.post("api/v2/auth/securereset", data=json.dumps({
            "email": "tevothuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_sending_mail_with_no_mail_prop(self):
        res = self.client.post("api/v2/auth/reset", data=json.dumps({
            "emai": "tevothuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_sending_mail_with_poorly_formatted_mail(self):
        res = self.client.post("api/v2/auth/reset", data=json.dumps({
            "email": "tevothukgmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_sending_mail_with_mail(self):

        self.client.post("api/v2/auth/signup",
                         data=json.dumps({
                             "username": "Tevyn",
                             "firstname": "Tevin",
                             "lastname": "Gach",
                             "email": "tevinthuku@gmail.com",
                             "phone": "0735464438",
                             "othername": "Thuku",
                             "password": "Tevinrocks1995",
                             "retypedpassword": "Tevinrocks1995",
                             "passportUrl": "http"
                         }),
                         content_type="application/json")
        res = self.client.post("api/v2/auth/reset", data=json.dumps({
            "email": "tevinthuku@gmail.com",
        }), content_type="application/json")
        self.assertEqual(res.status_code, 200)
