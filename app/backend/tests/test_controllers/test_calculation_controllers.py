import json
import unittest
from datetime import datetime

from falcon import testing, falcon

from tests import fixtures
from tests.fake_app_factory import TestCopyOriginalAppFactory


class TestCalculateVacationControllers(unittest.TestCase):
    def setUp(self):
        self.factory = TestCopyOriginalAppFactory()
        self.app = self.factory.create_app()
        self.client = testing.TestClient(self.app)

    def test_get_calculation(self):
        employee = fixtures.load('admin_user')
        saved_employee = self.factory.employee_storage.find_by_email(employee['email'])
        saved_employee.employment_date = datetime(2016, 8, 1)
        self.factory.employee_storage.update(saved_employee)
        headers = self.__get_authorization_header_for(employee)
        path = '/api/employees/{}/vacation'.format(employee['id'])
        body = json.dumps({'year': 2018, 'month': 1})
        response = self.client.simulate_post(path=path, body=body, headers=headers)

        self.assertEqual(response.status, falcon.HTTP_200)
        month_vacation = response.json['month_vacation']
        total_vacation = response.json['total_vacation']
        self.assertEqual(month_vacation, 3.29)
        self.assertEqual(total_vacation, 4.29)

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
