import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

created_to_category = {
    'category_name': 'Design'
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_category(self):
        response = self.client.get(
            "/category_config/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_list_category_single(self):
        response = self.client.get(
            "/category_config/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_add_category(self):
        response = self.client.post(
            "/category_config/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=created_to_category)
        assert response.status_code == 200

    def test_delete_category(self):
        response = self.client.delete(
            "/category_config/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_category(self):
        response = self.client.patch(
            "/category_config/94/",
            json=created_to_category,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_put_category(self):
        response = self.client.put(
            "/category_config/94/",
            json=created_to_category,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
