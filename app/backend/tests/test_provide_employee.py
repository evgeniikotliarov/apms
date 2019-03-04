import unittest
from _datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator
from domain.models.employee import Employee
from tests import fixtures


class ProvideEmployeeTestCase(unittest.TestCase):
    def test_create_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, "Some Name")
        self.assertEqual(employee.password, "some_password")
        self.assertEqual(employee.email, "some@email.com")
        self.assertEqual(employee.activated, False)
        self.assertEqual(employee.is_admin, False)

    def test_register_employee(self):
        employee = fixtures.load_instance("unaccepted_user", Employee)
        now_date = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now_date,
                                             balance_vac=5)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.acceptance_date.year, now_date.year)
        self.assertEqual(employee.acceptance_date.month, now_date.month)
        self.assertEqual(employee.acceptance_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.is_admin, False)
        self.assertEqual(employee.vacation, 5)

    def test_register_employee_without_balance_vacation(self):
        serialized_employee = fixtures.load("unaccepted_user")
        employee = EmployeeProvider.deserialize(serialized_employee)
        now_date = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now_date)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.acceptance_date.year, now_date.year)
        self.assertEqual(employee.acceptance_date.month, now_date.month)
        self.assertEqual(employee.acceptance_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.is_admin, False)
        self.assertEqual(employee.vacation, 0)

    def test_update_employee(self):
        serialized_employee = fixtures.load("unactivated_user")
        employee = EmployeeProvider.deserialize(serialized_employee)
        employee = EmployeeProvider.update_with(employee, name="New Name")
        self.assertEqual(employee.name, "New Name")

        employee = EmployeeProvider.update_with(employee, employment_date=datetime(2019, 1, 30))
        self.assertEqual(employee.employment_date, datetime(2019, 1, 30))
        self.assertEqual(employee.rate, RateCalculator.MAX_DAYS)

        employee = EmployeeProvider.update_with(employee, email="new@mail.com")
        self.assertEqual(employee.email, "new@mail.com")

        employee = EmployeeProvider.update_with(employee,
                                                password="new_password")
        self.assertEqual(employee.password, "new_password")

        employee = EmployeeProvider.activate(employee)
        self.assertEqual(employee.activated, True)

        employee = EmployeeProvider.deactivate(employee)
        self.assertEqual(employee.activated, False)

        self.assertEqual(employee.is_admin, False)

        employee = EmployeeProvider.set_balance_vac(employee, 10)
        self.assertEqual(employee.vacation, 10)

    def test_grant_to_admin_employee(self):
        serialized_employee = fixtures.load("unaccepted_user")
        employee = EmployeeProvider.deserialize(serialized_employee)
        employee = EmployeeProvider.grant_to_admin(employee)
        self.assertTrue(employee.is_admin)

    def test_pick_up_admin_employee(self):
        serialized_employee = fixtures.load("admin_user")
        employee = EmployeeProvider.deserialize(serialized_employee)
        employee = EmployeeProvider.pick_up_admin(employee)
        self.assertFalse(employee.is_admin)

    def test_serialize_employee(self):
        employee = fixtures.load_instance("unactivated_user", Employee)
        employee.employment_date = datetime(2019, 1, 1)
        employee.acceptance_date = datetime(2019, 1, 1)
        serialized_employee = EmployeeProvider.serialize(employee)
        self.assertIsNotNone(serialized_employee)
        self.assertEqual(serialized_employee['id'], 2)
        self.assertEqual(serialized_employee['name'], 'Unactivated User')
        self.assertEqual(serialized_employee['email'], 'unactivated@email.com')
        self.assertEqual("2019.01.01", serialized_employee['employment_date'])
        self.assertEqual("2019.01.01", serialized_employee['acceptance_date'])
        self.assertEqual(serialized_employee['vacation'], 1.0)
        self.assertEqual(serialized_employee['activated'], False)
        self.assertEqual(serialized_employee['is_admin'], False)

    def test_deserialize_employee(self):
        serialized_employee = fixtures.load("unactivated_user")
        employee = EmployeeProvider.deserialize(serialized_employee)

        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 2)
        self.assertEqual(employee.name, 'Unactivated User')
        self.assertEqual(employee.password, 'user')
        self.assertEqual(employee.email, 'unactivated@email.com')
        self.assertEqual(datetime(2019, 1, 1), employee.employment_date)
        self.assertEqual(datetime(2019, 1, 1), employee.acceptance_date)
        self.assertEqual(employee.vacation, 1.0)
        self.assertEqual(employee.activated, False)
        self.assertEqual(employee.is_admin, False)

    def test_serialize_unaccepted_employee(self):
        employee = fixtures.load_instance("unaccepted_user", Employee)
        serialized_employee = EmployeeProvider.serialize(employee)
        self.assertIsNotNone(serialized_employee)
        self.assertEqual(serialized_employee['id'], 1)
        self.assertEqual(serialized_employee['name'], 'Unregistered User')
        self.assertEqual(serialized_employee['email'], 'unaccepted@email.com')
        self.assertIsNone(serialized_employee['employment_date'])
        self.assertIsNone(serialized_employee['vacation'])
        self.assertFalse(serialized_employee['activated'])
        self.assertFalse(serialized_employee['is_admin'])

    def test_deserialize_unaccepted_employee(self):
        serialized_employee = fixtures.load("unaccepted_user")
        employee = EmployeeProvider.deserialize(serialized_employee)

        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 1)
        self.assertEqual(employee.name, 'Unregistered User')
        self.assertEqual(employee.password, 'user')
        self.assertEqual(employee.email, 'unaccepted@email.com')
        self.assertFalse(employee.activated)
        self.assertFalse(employee.is_admin)
        self.assertIsNone(employee.vacation)
        self.assertIsNone(employee.employment_date)
        self.assertIsNone(employee.acceptance_date)
