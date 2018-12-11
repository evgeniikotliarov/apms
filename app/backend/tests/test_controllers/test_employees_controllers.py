import json
import unittest

from falcon import testing, falcon

from tests import fixtures
from tests.fake_app_factory import TestCopyOriginalAppFactory


class TestEmployeesControllers(unittest.TestCase):
    def setUp(self):
        self.factory = TestCopyOriginalAppFactory()
        self.app = self.factory.create_app()
        self.client = testing.TestClient(self.app)

    def test_registration_user(self):
        data = {
            'name': 'employee_2',
            'password': 'password',
            'email': 'empl2@mail.com',
        }
        body = json.dumps(data)
        response = self.client.simulate_post('/api/sign-up', body=body)
        self.assertEqual(response.status, falcon.HTTP_201)
        self.assertIsNotNone(response.json['token'])

    def test_authentication_user(self):
        data = {
            'password': 'admin',
            'email': 'admin@email.com',
        }

        response = self.client.simulate_post('/api/sign-in', body=json.dumps(data))
        self.assertEqual(response.status, falcon.HTTP_200)
        self.assertIsNotNone(response.json['token'])

    def test_accept_user(self):
        admin = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(admin)

        unaccepted = fixtures.load('unaccepted_user')
        path = '/api/employees/{}/accept'.format(unaccepted['id'])

        body = json.dumps({'employment_date': '2018.1.2', 'vacation': '1'})
        response = self.client.simulate_post(path=path, body=body, headers=headers)
        self.assertEqual(response.status, falcon.HTTP_201)
        accepted_employee = self.factory.employee_storage.find_by_email(unaccepted['email'])
        self.assertEqual(accepted_employee.vacation, 1)
        self.assertEqual(accepted_employee.employment_date.year, 2018)
        self.assertEqual(accepted_employee.employment_date.month, 1)
        self.assertEqual(accepted_employee.employment_date.day, 2)
        self.assertTrue(accepted_employee.activated)

    def test_get_employee(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        response = self.client.simulate_get('/api/employees/0', headers=headers)
        del employee['password']
        self.assertEqual(response.json, employee)

    def test_get_employees(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        response = self.client.simulate_get('/api/employees/', headers=headers)
        self.assertTrue(response.json.__len__() > 0)
        first_employee = response.json[0]
        del employee['password']
        self.assertEqual(first_employee, employee)

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
