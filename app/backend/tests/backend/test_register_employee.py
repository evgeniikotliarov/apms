import unittest

from backend.tests.backend.fake_app_factory import TestAppFactory


class RegisterUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = TestAppFactory().create_app()

    def test_add_employee(self):
        employee = self.app.create_employee("Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")

    def test_register_employee(self):
        employee = self.app.create_employee("Some Name", "some_password", "some@email.com")
        self.app.create_employee("Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")

if __name__ == '__main__':
    unittest.main()
