import unittest

from domain.controllers.EmployeeProvider import EmployeeProvider


class RegisterUserTestCase(unittest.TestCase):
    def test_create_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")

if __name__ == '__main__':
    unittest.main()