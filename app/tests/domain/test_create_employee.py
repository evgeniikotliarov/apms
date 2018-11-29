import unittest
from _datetime import datetime

from domain.controllers.EmployeeProvider import EmployeeProvider


class CreateEmployeeTestCase(unittest.TestCase):
    def test_create_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")

    def test_register_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        now_date = datetime.now()
        employee = EmployeeProvider.register_user(employee=employee,
                                                  employment_date=now_date,
                                                  balance_vac=5)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.registration_date.year, now_date.year)
        self.assertEqual(employee.registration_date.month, now_date.month)
        self.assertEqual(employee.registration_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.vacation, 5)

    def test_register_employee_without_balance_vacation(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        now_date = datetime.now()
        employee = EmployeeProvider.register_user(employee=employee,
                                                  employment_date=now_date)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.registration_date.year, now_date.year)
        self.assertEqual(employee.registration_date.month, now_date.month)
        self.assertEqual(employee.registration_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.vacation, 0)

if __name__ == '__main__':
    unittest.main()
