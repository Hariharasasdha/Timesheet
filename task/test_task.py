import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

created_to_task = {
    'task_name': 'Q.A'
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_task(self):
        response = self.client.get(
            "/task/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_list_task_single(self):
        response = self.client.get(
            "/task/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_add_task(self):
        response = self.client.post(
            "/task/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=created_to_task)
        assert response.status_code == 200

    def test_delete_task(self):
        response = self.client.delete(
            "/task/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_task(self):
        response = self.client.patch(
            "/task/94/",
            json=created_to_task,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_put_task(self):
        response = self.client.put(
            "/task/94/",
            json=created_to_task,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
