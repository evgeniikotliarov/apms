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

    def test_get_day_of_time_sheet(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/time-sheets/{}/day/{}'.format(1, 1)
        response = self.client.simulate_get(path=path, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        day_value = response.json
        self.assertEqual(day_value, 1)

    def test_update_one_day(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/time-sheets/{}/day/{}'.format(1, 1)
        body = json.dumps({'value': 0.5})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json
        self.assertEqual(time_sheet['sheet'][0], 0.5)
        self.assertNotEqual(time_sheet['vacation'], 1.)

    def test_update_time_sheet_by_time_sheet_id(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/time-sheets/{}'.format(1)
        sheet = fixtures.load('full_january')
        body = json.dumps({'year': 2018, 'month': 1, 'sheet': sheet})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json
        self.assertEqual(time_sheet['sheet'], sheet)

    def test_update_time_sheet(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/{}/time-sheets'.format(employee['id'])
        sheet = fixtures.load('full_january')
        body = json.dumps({'year': 2018, 'month': 1, 'sheet': sheet})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        time_sheet = response.json
        self.assertEqual(time_sheet['sheet'], sheet)

    def test_update_time_sheet_without_data(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/{}/time-sheets'.format(employee['id'])
        sheet = fixtures.load('full_january')
        body = json.dumps({'year': 2018, 'sheet': sheet})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)
        self.assertEqual(response.status, falcon.HTTP_400)

        body = json.dumps({'month': 1, 'sheet': sheet})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)
        self.assertEqual(response.status, falcon.HTTP_400)

        body = json.dumps({'year': 2018, 'month': 1})
        response = self.client.simulate_patch(path=path, body=body, headers=headers)
        self.assertEqual(response.status, falcon.HTTP_400)

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
