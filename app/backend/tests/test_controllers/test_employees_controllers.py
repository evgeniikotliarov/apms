import json
import unittest

from falcon import testing, falcon

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
