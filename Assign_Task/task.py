import unittest
from ipss_utils.ipss_test import IpssTestCases
from app import create_app
import config

app = create_app(config.Config)

sample_data = {

    "task": "HRM",
    "sub_task": "Dashboard"

}


class AppTestCase(IpssTestCases):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_get_source(self):
        response = self.client.get(
            "/assign_task/",

            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_single_get_source(self):
        response = self.client.get(
            "/assign_task/6/",

            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        print(response.json)
        print(response.status_code)
        assert response.status_code == 200

    def test_post_source(self):
        response = self.client.post(
            "/assign_task/",
            json=sample_data,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        print(response.status_code)
        print(response.json)
        assert response.status_code == 200

    def test_delete_source(self):
        response = self.client.delete(
            "/assign_task/6/",

            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_source(self):
        response = self.client.patch(
            "/assign_task/6/",
            json=sample_data,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })
        print(response.json)
        assert response.status_code == 200

    def test_put_source(self):
        response = self.client.put(
            "/assign_task/6/",
            json=sample_data,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })
        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
