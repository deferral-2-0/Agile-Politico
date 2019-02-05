from app import app
import unittest
import json

from app.api.v1.model import PARTIES


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()

    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestPartiesEndpoints(RoutesBaseTest):

    def test_call_to_fetch_all_endpoints(self):
        response = self.client.get("api/v1/parties")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], [])
        self.assertEqual(result["status"], 200)
