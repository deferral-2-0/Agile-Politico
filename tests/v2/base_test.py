import unittest
import os
import json
from app.api.v2.models.db import init_db
from app import app

KEY = os.getenv('SECRET_KEY')
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


class BaseTestClass(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        init_db()
        admin = self.client.post("api/v2/auth/signup",
                                 data=json.dumps({
                                     "username": "AdminForTests",
                                     "firstname": "Tevin",
                                     "lastname": "Gach",
                                     "email": "tevinadmin@gmail.com",
                                     "phone": "0735464438",
                                     "othername": "Thuku",
                                     "password": "Tevin1995",
                                     "retypedpassword": "Tevin1995",
                                     "passportUrl": "http",
                                     "isPolitician": False,
                                     "isAdmin": True
                                 }),
                                 content_type="application/json")
        self.ADMIN_TOKEN = json.loads(
            admin.data.decode("utf-8"))["data"][0]["token"]

    def tearDown(self):
        """Clear the db after tests finish running"""
        init_db()
