import json
import unittest

from falcon import testing, falcon

from exceptions import DeactivatedEmployeeError
from tests import fixtures
from tests.fake_app_factory import TestCopyOriginalAppFactory
from utils.hash_maker import ToHash


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

        response = self.client.simulate_post('/api/log-in', body=json.dumps(data))
        self.assertEqual(response.status, falcon.HTTP_200)
        self.assertIsNotNone(response.json['token'])

    def test_authentication_deactivated_user(self):
        data = {
            'password': 'user',
            'email': 'unactivated@email.com',
        }

        response = self.client.simulate_post('/api/log-in', body=json.dumps(data))
        self.assertEqual(response.status, DeactivatedEmployeeError().get_http_code())

    def test_register_user(self):
        admin = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(admin)

        unaccepted = fixtures.load('unaccepted_user')
        path = '/api/employees/{}/register'.format(unaccepted['id'])

        body = json.dumps({'employment_date': '2018.1.2', 'vacation': '1'})
        response = self.client.simulate_post(path=path, body=body, headers=headers)
        self.assertEqual(response.status, falcon.HTTP_201)
        accepted_employee = self.factory.employee_storage.find_by_email(unaccepted['email'])
        self.assertEqual(accepted_employee.vacation, 1)
        self.assertEqual(accepted_employee.employment_date.year, 2018)
        self.assertEqual(accepted_employee.employment_date.month, 1)
        self.assertEqual(accepted_employee.employment_date.day, 2)
        self.assertTrue(accepted_employee.activated)

    def test_get_profile(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        response = self.client.simulate_get('/api/profile', headers=headers)
        del employee['password']
        employee['rate'] = 10
        self.assertEqual(response.json, employee)

    def test_get_employee(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        response = self.client.simulate_get('/api/employees/0', headers=headers)
        del employee['password']
        employee['rate'] = 10
        self.assertEqual(response.json, employee)

    def test_get_employees(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        response = self.client.simulate_get('/api/employees/', headers=headers)
        self.assertTrue(response.json.__len__() > 0)
        first_employee = response.json[0]
        del employee['password']
        employee['rate'] = 10
        self.assertEqual(first_employee, employee)

    def test_update_profile(self):
        employee = fixtures.load('admin_user')
        headers = self.__get_authorization_header_for(employee)
        to_hash = ToHash()

        body = json.dumps({
            'name': 'new name',
            'old_password': 'admin',
            'new_password': 'new pass'
        })
        response = self.client.simulate_patch('/api/profile', headers=headers, body=body)

        self.assertEqual(response.json['name'], 'new name')
        self.assertEqual(response.json['email'], employee['email'])

        updated_employee = self.factory.employee_storage.find_by_id(0)
        self.assertTrue(to_hash.check_with_hash('new pass', updated_employee.password))

        body = json.dumps({'name': 'the newest name'})
        response = self.client.simulate_patch('/api/profile', headers=headers, body=body)

        self.assertEqual(response.status, falcon.HTTP_200)
        self.assertEqual(response.json['name'], 'the newest name')
        self.assertEqual(response.json['email'], employee['email'])

        updated_employee = self.factory.employee_storage.find_by_id(0)
        self.assertTrue(to_hash.check_with_hash('new pass', updated_employee.password))

        body = json.dumps({
            'name': 'admin',
            'email': 'admin@email.com',
            'old_password': 'new pass',
            'new_password': 'admin',
        })
        response = self.client.simulate_patch('/api/profile', headers=headers, body=body)

        self.assertEqual(response.json['name'], 'admin')
        self.assertEqual(response.json['email'], 'admin@email.com')

        updated_employee = self.factory.employee_storage.find_by_id(0)
        self.assertTrue(to_hash.check_with_hash('admin', updated_employee.password))

    def __get_authorization_header_for(self, employee):
        email = employee['email']
        token = self.factory.tokens[email]
        return {'Authorization': token}
