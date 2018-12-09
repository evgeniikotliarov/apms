import unittest
from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from storages.storages import EmployeesStorage
from tests import fixtures
from tests.fake_db import FakeDb
from usecases.employee_use_cases import CreateEmployeeUseCase, RegisterEmployeeUseCase, \
    UpdateEmployeeUseCase, AdminRightsEmployeeUseCase, GetEmployeeUseCase, GetAllEmployeeUseCase


class TestProvideEmployeeUseCase(unittest.TestCase):
    def test_get_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = GetEmployeeUseCase(controller, storage)

        saved_employee = use_case.get_employee(employee_id=0)
        self.assertEqual(saved_employee['name'], "admin")
        self.assertEqual(saved_employee['email'], "admin@email.com")
        self.assertEqual(saved_employee['activated'], True)

    def test_get_all_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = GetAllEmployeeUseCase(controller, storage)

        employees = use_case.get_employees()
        self.assertEqual(employees.__len__(), 3)
        saved_employee = employees[0]
        self.assertEqual(saved_employee['name'], "admin")
        self.assertEqual(saved_employee['email'], "admin@email.com")
        self.assertEqual(saved_employee['activated'], True)
        self.assertEqual(saved_employee['vacation'], 1.0)

    def test_create_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = CreateEmployeeUseCase(controller, storage)

        use_case.create_employee("some name", password="some password", email="user1@email.com")
        saved_employee = storage.find_by_email("user1@email.com")
        self.assertEqual(saved_employee.name, "some name")
        self.assertEqual(saved_employee.password, "some password")
        self.assertEqual(saved_employee.email, "user1@email.com")

        use_case.create_employee("new user", "some password", "user2@email.com")
        saved_employee = storage.find_by_email("user2@email.com")
        self.assertEqual(saved_employee.name, "new user")
        self.assertEqual(saved_employee.password, "some password")
        self.assertEqual(saved_employee.email, "user2@email.com")
        self.assertEqual(saved_employee.activated, False)

    def test_register_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = RegisterEmployeeUseCase(controller, storage)

        now = datetime.now()
        serialized_employee = fixtures.load("unregistered_user")
        use_case.register_employee(serialized_employee["id"], employment_date=now)

        saved_employee = storage.find_by_email(serialized_employee["email"])
        self.assertEqual(saved_employee.employment_date, now)
        self.assertEqual(saved_employee.vacation, 0)
        self.assertEqual(saved_employee.activated, True)

    def test_update_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = UpdateEmployeeUseCase(controller, storage)
        use_case.update_employee(0, "new name", "new password", "new@email.com")

        saved_employee = storage.find_by_id(0)
        self.assertEqual(saved_employee.name, "new name")
        self.assertEqual(saved_employee.password, "new password")
        self.assertEqual(saved_employee.email, "new@email.com")
        self.assertEqual(saved_employee.activated, True)

    def test_admin_rights_employee(self):
        storage = EmployeesStorage(FakeDb().build())
        controller = EmployeeProvider()
        use_case = AdminRightsEmployeeUseCase(controller, storage)

        saved_employee = storage.find_by_id(1)
        self.assertEqual(saved_employee.is_admin, False)

        use_case.grant_to_admin(1)
        saved_employee = storage.find_by_id(1)
        self.assertEqual(saved_employee.is_admin, True)

        use_case.pick_up_admin(1)
        saved_employee = storage.find_by_id(1)
        self.assertEqual(saved_employee.is_admin, False)
