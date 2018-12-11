import json
import unittest

from falcon import testing, falcon

from domain.controllers.rate_calculator import RateCalculator
from tests import fixtures
from tests.fake_app_factory import TestCopyOriginalAppFactory


class TestEmployeesControllers(unittest.TestCase):
    def setUp(self):
        self.factory = TestCopyOriginalAppFactory()
        self.app = self.factory.create_app()
        self.client = testing.TestClient(self.app)

    def test_get_time_sheets_for_employee(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/{}/time-sheets'.format(employee['id'])
        body = json.dumps({'year': 2018, 'month': 1})
        response = self.client.simulate_post(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json[0]
        self.assertEqual(time_sheet['employee_id'], employee['id'])
        self.assertEqual(time_sheet['norm'], 23)
        self.assertEqual(time_sheet['rate'], RateCalculator.MIN_DAYS)
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['closed'], False)

        body = json.dumps({'year': 2018})
        response = self.client.simulate_post(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json[0]
        self.assertEqual(time_sheet['employee_id'], employee['id'])
        self.assertEqual(time_sheet['norm'], 23)
        self.assertEqual(time_sheet['rate'], RateCalculator.MIN_DAYS)
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['closed'], False)

    def test_get_time_sheet_for_employees(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/time-sheets'
        body = json.dumps({'year': 2018, 'month': 1})
        response = self.client.simulate_post(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json[0]
        self.assertEqual(time_sheet['norm'], 23)
        self.assertEqual(time_sheet['rate'], RateCalculator.MIN_DAYS)
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['closed'], False)

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
