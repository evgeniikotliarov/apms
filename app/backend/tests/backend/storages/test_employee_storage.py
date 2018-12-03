import unittest

from domain.controllers.employee_provider import EmployeeProvider
from storages.storages import EmployeesStorage
# noinspection PyPackageRequirements
from tests.fake_db import FakeEmployeesDb


class TestEmployeesStorage(unittest.TestCase):
    def test_get_employee(self):
        storage = EmployeesStorage(FakeEmployeesDb())
        employee = storage.find_by_id(0)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertIsNotNone(employee.name)
        self.assertIsNotNone(employee.email)
        self.assertIsNotNone(employee.password)

    def test_get_all_employee(self):
        storage = EmployeesStorage(FakeEmployeesDb())
        employees = storage.get_all()
        self.assertIsNotNone(employees)
        employee = employees.first()
        self.assertEqual(employee.id, 0)
        self.assertIsNotNone(employee.name)
        self.assertIsNotNone(employee.email)
        self.assertIsNotNone(employee.password)

    def test_save_employees(self):
        employee = EmployeeProvider.create_simple("some name", "some password", "some@email.com")
        employee.id = 75
        storage = EmployeesStorage(FakeEmployeesDb())
        storage.save(employee)
        employee = storage.find_by_id(75)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 75)
        self.assertEqual(employee.name, "some name")
        self.assertEqual(employee.email, "some@email.com")
        self.assertEqual(employee.password, "some password")

    def test_update_employee(self):
        storage = EmployeesStorage(FakeEmployeesDb())
        employee = storage.find_by_id(0)
        employee.name = "Updated Name"
        employee.password = "Updated Password"
        storage.update(employee)

        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Updated Name")
        self.assertEqual(employee.email, "some@mail.com")
        self.assertEqual(employee.password, "Updated Password")
