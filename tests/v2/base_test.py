import unittest
import os
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

    def tearDown(self):
        """Clear the db after tests finish running"""
        init_db()
