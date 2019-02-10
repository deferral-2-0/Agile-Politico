from app import app
import unittest
import json


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestOfficesEndPoint(RoutesBaseTest):

    def test_invalid_route(self):
        response = self.client.get("api/vNotFound")
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result["error"], "url not found")
        self.assertEqual(result["status"], 404)

    def test_method_not_allowed(self):
        response = self.client.post("api/v1/offices/0")
        self.assertEqual(response.status_code, 405)
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["status"], 405)
