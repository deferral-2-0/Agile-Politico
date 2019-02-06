from app import app
import unittest
import json

from app.api.v1.model import OFFICES


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.office1 = {
            "id": 0,
            "type": "Governor",
            "name": "Governor Webuye"
        }
        self.erroroffice = {
            "id": 1
        }
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestOfficesEndPoint(RoutesBaseTest):

    def test_fetch_all_offices(self):
        response = self.client.get("api/v1/offices")
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["data"], [])
        self.assertEqual(result["status"], 200)

    def test_save_office(self):
        res = self.client.post(
            "api/v1/offices", data=json.dumps(self.office1), content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 201)
        self.assertEqual(len(OFFICES), 2)

    def test_save_missing_fields_office(self):
        res = self.client.post(
            "api/v1/offices", data=json.dumps(self.erroroffice), content_type="application/json")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result['status'], 400)

    def test_getting_specific_office(self):
        self.client.post(
            "api/v1/offices", data=json.dumps(self.office1), content_type="application/json")
        res = self.client.get("/api/v1/offices/0")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result["data"], [{
            "id": 0,
            "type": "Governor",
            "name": "Governor Webuye"
        }])
        self.assertEqual(result["status"], 200)

    def test_getting_non_existent_office(self):
        res = self.client.get("/api/v1/offices/10")
        self.assertEqual(res.status_code, 404)
