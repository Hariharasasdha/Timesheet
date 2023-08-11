import json
import unittest

from ipss_utils.ipss_test import IpssTestCases

from app import create_app
import config

app = create_app(config.Config)

timesheet = {
    "emp_id": 2721,
    "from_date": "2022-12-05",
    "to_date": "2022-12-11",
    "date": "Weekend 5th December",
    "total_hrs": "6",
    'compcode': 1539147649705,
    "selfLists": [
        {
            "task_id": 48,
            "sub_task_id": 48,
            "category_id": 48,
            "description": "ui",
            "monday": "2",
            "hrs_per_task": "2",
'compcode': 1539147649705
        }, {

            "task_id": 15,
            "sub_task_id": 15,
            "category_id": 15,
            "description": "bug",
'compcode': 1539147649705,
            "tuesday": "4",
            "hrs_per_task": "2"
        }

    ]
}


class AppTestCase(IpssTestCases):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        super(AppTestCase, self).setUp()

    def test_list_timesheet(self):
        response = self.client.get(
            "/timesheet/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        print(response.json)
        assert response.status_code == 200

    def test_list_timesheet_single(self):
        response = self.client.get(
            "/timesheet/33/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            }
        )
        print(response.json)
        assert response.status_code == 200

    def test_add_timesheet(self):
        response = self.client.post(
            "/timesheet/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            },

            json=timesheet)
        assert response.status_code == 200

    def test_delete_timesheet(self):
        response = self.client.delete(
            "/timesheet/33/",
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })

        assert response.status_code == 200

    # def test_patch_vehicle(self):
    #     response = self.client.patch(
    #         "/vehicles/94/",
    #         json=timesheet,
    #         headers={
    #             'Authorization': f"Bearer {self.access_token}"
    #         })
    #
    #     assert response.status_code == 200

    def test_put_timesheet(self):
        response = self.client.put(
            "/timesheet/33/",
            json=timesheet,
            headers={
                'Authorization': f"Bearer {self.access_token}"
            })
        print(response.json)
        assert response.status_code == 200


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(AppTestCase())
    unittest.TextTestRunner().run(suite)
