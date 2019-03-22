import unittest
import os
import json
from app.api.v2.models.db import init_db
from app import app

import io

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
        admin = self.client.post("api/v2/auth/signin",
                                 data=json.dumps({
                                     "email": "admindetails@gmail.com",
                                     "password": "BootcampWeek1"
                                 }),
                                 content_type="application/json")
        self.ADMIN_TOKEN = json.loads(
            admin.data.decode("utf-8"))["data"]["token"]
        self.setUpFileUpload()

    def setUpFileUpload(self):
        """
            Creates a simulated file for use in testing for file parts
            in requests.
        """
        self.file_object = {
            'image': (io.BytesIO(b'cool looking pic'), 'test_file1.gif')
        }

    def post(self, path, data, content='application/json', headers=None):
        """
            Performs a POST request for sending of multiple test requests,.
        """
        if not headers:
            headers = self.ADMIN_TOKEN
        res = self.client.post(path, data=data,
                               content_type=content,
                               headers=headers)
        return res

    def tearDown(self):
        """Clear the db after tests finish running"""
        init_db()
