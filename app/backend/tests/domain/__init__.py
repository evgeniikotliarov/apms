import unittest

from backend.domain.controllers.employee_provider import EmployeeProvider


class RegisterUserTestCase(unittest.TestCase):
    def test_create_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "Some Password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "Some Password")
        self.assertEqual(employee.email, "some@email.com")

if __name__ == '__main__':
    unittest.main()
