import json

from tests.v2.base_test import BaseTestClass

import os
KEY = os.getenv('SECRET_KEY')


class TestUserEndpoints(BaseTestClass):
    def test_get_feedback(self):
        res = self.client.get("api/v2/feedback")
        self.assertEqual(res.status_code, 200)

    def test_post_feedback(self):
        res = self.client.post(
            "api/v2/feedback",
            data=json.dumps({
                "body": "The process is nice so far..."
            }),
            headers={'x-access-token': self.ADMIN_TOKEN},
            content_type="application/json")
        self.assertEqual(res.status_code, 201)
