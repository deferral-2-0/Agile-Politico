from app import app
import unittest
import json

from app.api.v1.model import OFFICES


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.party1 = {
            "id": 0,
            "type": "Governor",
            "name": "Governor Webuye"
        }
        self.falseparty = {
            "id": 1
        }
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestOfficesAPI(RoutesBaseTest):

    def test_call_to_fetch_all_offices(self):
        response = self.client.get("api/v1/offices")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], [])
        self.assertEqual(result["status"], 200)

    def test_saving_office(self):
        res = self.client.post(
            "api/v1/offices", data=json.dumps(self.party1), content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(len(OFFICES), 1)

    def test_wrongly_formatted_office(self):
        res = self.client.post(
            "api/v1/offices", data=json.dumps(self.falseparty), content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 400)
