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

    def test_get_time_sheet(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/time-sheets/{}'.format(1)
        response = self.client.simulate_get(path=path, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)

        time_sheet = response.json
        saved_time_sheet = self.factory.time_sheet_storage.find_by_id(1)

        self.assertEqual(time_sheet['sheet'], saved_time_sheet.sheet)

    def test_update_one_day(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/time-sheets/{}'.format(1)
        body = json.dumps({'day': 1, 'value': 0.5})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = self.factory.time_sheet_storage.find_by_id(1)
        self.assertEqual(time_sheet.sheet[0], 0.5)

    def test_update_time_sheet(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/{}/time-sheets'.format(employee['id'])
        sheet = fixtures.load('full_january')
        body = json.dumps({'year': 2018, 'month': 1, 'sheet': sheet})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = self.factory.time_sheet_storage.find_by(
            employee_id=employee['id'],
            year=2018,
            month=1)[0]
        self.assertEqual(time_sheet.sheet, sheet)

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
