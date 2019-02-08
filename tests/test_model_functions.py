
# from app import app
# import unittest
# import json
# from flask import make_response, jsonify
# from app.api.utils import response_fn


# class RoutesBaseTest(unittest.TestCase):
#     def setUp(self):
#         self.app = app("testing")
#         self.client = self.app.test_client()
#     # tear down tests

#     def tearDown(self):
#         """Tperform final cleanup after tests run"""
#         self.app.testing = False


# class TestOfficesEndPoint(RoutesBaseTest):

#     def test_200_response(self):
#         assert(response_fn(200, "data", "Testing 202")) == make_response(jsonify({
#             "status": 200,
#             "data": "Testing 202"
#         }), 200)

#     def test_404_response(self):
#         assert(response_fn(404, "error", "An error occured")) == make_response(jsonify({
#             "status": 404,
#             "error": "An error occured"
#         }), 404)
