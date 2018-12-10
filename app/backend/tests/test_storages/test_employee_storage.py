import unittest

from domain.controllers.employee_provider import EmployeeProvider
from storages.storages import EmployeesStorage
from tests.fake_db import FakeDb


class TestEmployeesStorage(unittest.TestCase):
    def test_get_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        employee = storage.find_by_id(0)
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertIsNotNone(employee.name)
        self.assertIsNotNone(employee.email)
        self.assertIsNotNone(employee.password)

    def test_get_all_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        employees = storage.get_all()
        self.assertIsNotNone(employees)
        employee = employees[0]
        self.assertEqual(employee.id, 0)
        self.assertIsNotNone(employee.name)
        self.assertIsNotNone(employee.email)
        self.assertIsNotNone(employee.password)

    def test_save_employees(self):
        storage = EmployeesStorage(FakeDb().build())
        employee = EmployeeProvider.create_simple("some name", "some password", "some_1@email.com")
        storage.save(employee)
        saved_employee = storage.find_by_email("some_1@email.com")
        self.assertIsNotNone(saved_employee)
        self.assertEqual(saved_employee.id, employee.id)
        self.assertEqual(saved_employee.name, employee.name)
        self.assertEqual(saved_employee.email, employee.email)
        self.assertEqual(saved_employee.password, employee.password)

    def test_update_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        employee = storage.find_by_id(0)
        employee.name = "Updated Name"
        employee.password = "Updated Password"
        storage.update(employee)

        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, 0)
        self.assertEqual(employee.name, "Updated Name")
        self.assertEqual(employee.email, "admin@email.com")
        self.assertEqual(employee.password, "Updated Password")
