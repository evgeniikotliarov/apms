import unittest
from _datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator


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
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
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
        self.assertEqual(employee.is_admin, False)
        self.assertEqual(employee.vacation, 5)

    def test_register_employee_without_balance_vacation(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        now_date = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now_date)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.registration_date.year, now_date.year)
        self.assertEqual(employee.registration_date.month, now_date.month)
        self.assertEqual(employee.registration_date.day, now_date.day)
        self.assertEqual(employee.employment_date, now_date)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.is_admin, False)
        self.assertEqual(employee.vacation, 0)

    def test_update_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
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

        employee = EmployeeProvider.activate(employee)
        self.assertEqual(employee.activated, True)

        employee = EmployeeProvider.deactivate(employee)
        self.assertEqual(employee.activated, False)

        self.assertEqual(employee.is_admin, False)

        employee = EmployeeProvider.set_balance_vac(employee, 10)
        self.assertEqual(employee.vacation, 10)

    def test_grant_to_admin_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=datetime.now())
        employee = EmployeeProvider.grant_to_admin(employee)
        self.assertTrue(employee.is_admin)

    def test_pick_up_admin_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=datetime.now())
        employee.is_admin = True
        employee = EmployeeProvider.pick_up_admin(employee)
        self.assertFalse(employee.is_admin)

    def test_serialize_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        now = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now,
                                             balance_vac=5)
        serialized_employee = EmployeeProvider.serialize(employee)
        self.assertIsNotNone(serialized_employee)
        self.assertEqual(serialized_employee['id'], None)
        self.assertEqual(serialized_employee['name'], 'Some Name')
        self.assertEqual(serialized_employee['password'], 'some_password')
        self.assertEqual(serialized_employee['email'], 'some@email.com')
        self.assertTrue(str(now.year) in serialized_employee['employment_date'])
        self.assertTrue(str(now.month) in serialized_employee['employment_date'])
        self.assertTrue(str(now.day) in serialized_employee['employment_date'])
        self.assertIsNotNone(serialized_employee['registration_date'])
        self.assertEqual(serialized_employee['vacation'], 5)
        self.assertEqual(serialized_employee['activated'], True)
        self.assertEqual(serialized_employee['is_admin'], False)

    def test_deserialize_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        now = datetime.now()
        employee = EmployeeProvider.register(employee=employee,
                                             employment_date=now,
                                             balance_vac=5)
        serialized_employee = EmployeeProvider.serialize(employee)
        employee = EmployeeProvider.deserialize(serialized_employee)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, None)
        self.assertEqual(employee.name, 'Some Name')
        self.assertEqual(employee.password, 'some_password')
        self.assertEqual(employee.email, 'some@email.com')
        self.assertTrue(str(now.year), employee.employment_date)
        self.assertTrue(str(now.month), employee.employment_date)
        self.assertTrue(str(now.day), employee.employment_date)
        self.assertIsNotNone(employee.registration_date)
        self.assertEqual(employee.vacation, 5)
        self.assertEqual(employee.activated, True)
        self.assertEqual(employee.is_admin, False)

    def test_serialize_unregistered_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        serialized_employee = EmployeeProvider.serialize(employee)
        self.assertIsNotNone(serialized_employee)
        self.assertEqual(serialized_employee['id'], None)
        self.assertEqual(serialized_employee['name'], 'Some Name')
        self.assertEqual(serialized_employee['password'], 'some_password')
        self.assertEqual(serialized_employee['email'], 'some@email.com')
        self.assertEqual(serialized_employee['employment_date'], None)
        self.assertEqual(serialized_employee['vacation'], None)
        self.assertEqual(serialized_employee['activated'], False)
        self.assertEqual(serialized_employee['is_admin'], False)

    def test_deserialize_unregistered_employee(self):
        employee = EmployeeProvider.create_simple("Some Name", "some_password", "some@email.com")
        serialized_employee = EmployeeProvider.serialize(employee)
        employee = EmployeeProvider.deserialize(serialized_employee)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, None)
        self.assertEqual(employee.name, 'Some Name')
        self.assertEqual(employee.password, 'some_password')
        self.assertEqual(employee.email, 'some@email.com')
        self.assertEqual(employee.employment_date, None)
        self.assertEqual(employee.vacation, None)
        self.assertEqual(employee.activated, False)
        self.assertEqual(employee.is_admin, False)
