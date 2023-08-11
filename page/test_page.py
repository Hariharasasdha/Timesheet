import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

created_to_page = {
    'page_name': 'CRUD'
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_page(self):
        response = self.client.get(
            "/page_config/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_list_page_single(self):
        response = self.client.get(
            "/page_config/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_add_page(self):
        response = self.client.post(
            "/page_config/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=created_to_page)
        assert response.status_code == 200

    def test_delete_page(self):
        response = self.client.delete(
            "/page_config/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_page(self):
        response = self.client.patch(
            "/page_config/94/",
            json=created_to_page,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_put_page(self):
        response = self.client.put(
            "/page_config/94/",
            json=created_to_page,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
