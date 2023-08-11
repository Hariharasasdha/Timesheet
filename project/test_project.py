import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

created_to_project = {
    'project_name': 'HRM'
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_project(self):
        response = self.client.get(
            "/project/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_list_project_single(self):
        response = self.client.get(
            "/project/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_add_project(self):
        response = self.client.post(
            "/project/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=created_to_project)
        assert response.status_code == 200

    def test_delete_project(self):
        response = self.client.delete(
            "/project/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_project(self):
        response = self.client.patch(
            "/project/94/",
            json=created_to_project,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_put_project(self):
        response = self.client.put(
            "/project/94/",
            json=created_to_project,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
