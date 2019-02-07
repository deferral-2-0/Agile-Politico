from app import app
import unittest
import json

from app.api.v1.model import PARTIES


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
        self.party1 = {
            "name": "Party 1",
            "logoUrl": ""
        }
        self.partytodelete = {
            "name": "Party 10",
            "logoUrl": ""
        }
        self.invalidparty = {
            "_id": 1
        }

    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestPartiesEndpoints(RoutesBaseTest):

    def test_fetch_all_parties(self):
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

    def test_saving_missing_fields_party(self):
        res = self.client.post(
            "api/v1/parties", data=json.dumps(self.invalidparty), content_type="application/json")
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(result["status"], 400)

    def test_get_specific_party(self):
        createparty = self.client.post(
            "api/v1/parties", data=json.dumps(self.party1), content_type="application/json")
        json.loads(createparty.data.decode("utf-8"))
        res = self.client.get("/api/v1/parties/0")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result["data"], [{
            "id": 0,
            "name": "Party 1",
            "logoUrl": ""
        }])
        self.assertEqual(result["status"], 200)

    def test_getting_non_exiistent_party(self):
        res = self.client.get("/api/v1/parties/1000")
        result = json.loads(res.data.decode('utf-8'))
        self.assertEqual(result["status"], 404)

    def test_updating_party(self):
        res = self.client.patch("/api/v1/parties/{}/name".format(0),
                                data=json.dumps({
                                    "name": "New Name"
                                }), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_updating_party_with_invalid_params(self):
        res = self.client.patch("/api/v1/parties/{}/name".format(0),
                                data=json.dumps({
                                    "namehehre": "New Name"
                                }), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test_updating_non_exisitent_party(self):
        res = self.client.patch("/api/v1/parties/{}/name".format(1000),
                                data=json.dumps({
                                    "name": "New Name"
                                }), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test_deleting_party(self):
        self.client.post(
            "api/v1/parties", data=json.dumps(self.partytodelete), content_type="application/json")
        res = self.client.delete(
            "/api/v1/parties/{}".format(0), content_type="application/json")
        self.assertEqual(res.status_code, 200)

    def test_deleting_non_existent_party(self):
        res = self.client.delete(
            "/api/v1/parties/{}".format(1000), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(len(PARTIES), 0)
