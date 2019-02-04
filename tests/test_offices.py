from app import app
import unittest


class RoutesBaseTest(unittest.TestCase):
    def setUp(self):
        self.app = app("testing")
        self.client = self.app.test_client()
    # tear down tests

    def tearDown(self):
        """Tperform final cleanup after tests run"""
        self.app.testing = False


class TestQuestionsApiEndpoint(RoutesBaseTest):

    def test_api_v1_questions_response_status_code(self):
        response = self.client.get("api/v1/offices")
        self.assertEqual(response.status_code, 200)
