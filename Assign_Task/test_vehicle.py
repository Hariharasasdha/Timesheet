import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

Created_to_vehicle = {
      # "hrvehiclemastid": 94,
      "vehiclename": "fc",
      "vehicleroot": "400",
      "vehicleno": "TN956878",
      "vehiclecatgory": "Personal",
      "vehicletype": "Two Wheeler",
      "compcode": 1539147649705,
      "modified_by": "ithod@pgc.com",
      "modified_on": "2022-06-26 12:56:06",
      "created_by": "ithod@pgc.com",
      "created_on": "2022-06-24 05:38:25",
      "docdate": "2022-06-02 00:00:00",
      "docid": "PIII-00000085",
      "target": 0,
      "km": 0,
      "rootno": 0,
      "ownername": "sundar",
      "vrent": 500,
      "drivername": "ramkumar",
      "travelsname": "sundhar"
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_vehicle(self):
        response = self.client.get(
            "/vehicles/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_list_vehicle_single(self):
        response = self.client.get(
            "/vehicles/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        assert response.status_code == 200

    def test_add_vehicle(self):
        response = self.client.post(
            "/vehicles/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=Created_to_vehicle)
        assert response.status_code == 200

    def test_delete_vehicle(self):
        response = self.client.delete(
            "/vehicles/94/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_patch_vehicle(self):
        response = self.client.patch(
            "/vehicles/94/",
            json=Created_to_vehicle,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    def test_put_vehicle(self):
        response = self.client.put(
            "/vehicles/94/",
            json=Created_to_vehicle,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200




if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
