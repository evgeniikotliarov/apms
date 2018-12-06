import json
import unittest

from falcon import testing, falcon

from tests.fake_app_factory import TestCopyOriginalAppFactory


class TestEmployeesControllers(unittest.TestCase):
    def setUp(self):
        self.factory = TestCopyOriginalAppFactory()
        self.app = self.factory.create_app()
        self.client = testing.TestClient(self.app)

        self.employee = {
            'id': 1,
            'name': 'name',
            'password': 'password',
            'email': 'some@mail.com',
            'activated': False,
            'employment_date': None,
            'registration_date': None,
            'vacation': None,
            'is_admin': False
        }

    def test_get_employee(self):
        response = self.client.simulate_get('/api/employees/1')
        self.assertEqual(response.json, self.employee)

    def test_get_employees(self):
        response = self.client.simulate_get('/api/employees/')
        first_employee = response.json[0]
        self.assertEqual(first_employee, self.employee)

    def test_create_employee(self):
        data = {
            'name': 'employee_2',
            'password': 'password',
            'email': 'empl2@mail.com',
        }
        response = self.client.simulate_post('/api/employees/create', body=json.dumps(data))
        self.assertEqual(response.status, falcon.HTTP_201)
        response = self.client.simulate_get('/api/employees/2')
        self.assertEqual(response.json['name'], data['name'])
        self.assertEqual(response.json['email'], data['email'])
