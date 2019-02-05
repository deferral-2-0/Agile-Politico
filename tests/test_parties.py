from app import app
import unittest
import json

from app.api.v1.model import PARTIES


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.party1 = {
            "id": 0,
            "name": "Party 1",
            "logoUrl": "https:://img.party1.jpeg"
        }

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

    def test_saving_party(self):
        res = self.client.post(
            "api/v1/parties", data=json.dumps(self.party1), content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(len(PARTIES), 2)
