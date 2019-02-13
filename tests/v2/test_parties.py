"""Tests for password reset """
import json
import unittest

from app import app
from config import app_config
from app.api.v2.models.db import init_db


class BaseTestClass(unittest.TestCase):
    """
    Setting up tests
    """

    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.DB_URL = app_config['TEST_DB_URL']
        init_db(self.DB_URL)

    def tearDown(self):
        """Clear the db after tests finish running"""
        self.app.testing = False
        init_db(self.DB_URL)


class TestPartiesFunctionality(BaseTestClass):
    def test_fetching_all_parties(self):
        response = self.client.get("api/v2/parties",
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 200)
