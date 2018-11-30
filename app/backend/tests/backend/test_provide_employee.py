import unittest
from _datetime import datetime

from backend.domain.controllers.employee_provider import EmployeeProvider
from backend.domain.controllers.rate_calculator import RateCalculator


class ProvideEmployeeTestCase(unittest.TestCase):
    def test_create_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")
        self.assertEqual(employee.activated, False)

    def test_register_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        now_date = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now_date,
                                             balance_vac=5)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.registration_date.year, now_date.year)
        self.assertEqual(employee.registration_date.month, now_date.month)
        self.assertEqual(employee.registration_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.vacation, 5)

    def test_register_employee_without_balance_vacation(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        now_date = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now_date)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.registration_date.year, now_date.year)
        self.assertEqual(employee.registration_date.month, now_date.month)
        self.assertEqual(employee.registration_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.vacation, 0)

    def test_update_employee(self):
        employee = EmployeeProvider.create_simple(0, "Some Name", "some_password", "some@email.com")
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=datetime.now())
        employee = EmployeeProvider.update_with(employee, name="New Name")
        self.assertEqual(employee.name, "New Name")

        employee = EmployeeProvider.update_with(employee, employment_date=datetime(2018, 1, 30))
        self.assertEqual(employee.employment_date, datetime(2018, 1, 30))
        self.assertEqual(employee.rate, RateCalculator.MAX_DAYS)

        employee = EmployeeProvider.update_with(employee, email="new@mail.com")
        self.assertEqual(employee.email, "new@mail.com")

        employee = EmployeeProvider.update_with(employee, password="new_password")
        self.assertEqual(employee.password, "new_password")
