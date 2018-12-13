import unittest
from datetime import datetime

from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage
from tests.fake_db import FakeDb
from usecases.calculate_vacation_use_case import CalculateVacationUseCase


class TestProvideEmployeeUseCase(unittest.TestCase):
    def setUp(self):
        db = FakeDb().build()
        self.employee_storage = EmployeesStorage(db)
        self.time_sheet_storage = TimeSheetsStorage(db)
        self.calculator = VacationCalculator()
        self.use_case = CalculateVacationUseCase(self.calculator,
                                                 self.employee_storage,
                                                 self.time_sheet_storage)

    def test_calculate_vacation(self):
        employee = self.employee_storage.find_by_email("admin@email.com")
        employee.employment_date = datetime(2016, 8, 1)
        employee.vacation = 10
        self.employee_storage.update(employee)
        self.use_case.calculate_vacation(0)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 13.29)
        saved_time_sheet = self.time_sheet_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.vacation, 3.29)

        employee = self.employee_storage.find_by_email("with.vacation@email.com")
        employee.employment_date = datetime.today()
        self.employee_storage.update(employee)
        time_sheet = self.time_sheet_storage.find_by_id(0)
        time_sheet.employee_id = 3
        time_sheet.vacation = 0
        self.time_sheet_storage.update(time_sheet)
        self.use_case.calculate_vacation(0)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 12.3)
        saved_time_sheet = self.time_sheet_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.vacation, 2.3)

    def test_calculate_vacation_with_minus(self):
        employee = self.employee_storage.find_by_email('admin@email.com')
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        time_sheet = self.time_sheet_storage.find_by_id(1)
        time_sheet.employee_id = 0
        self.time_sheet_storage.update(time_sheet)
        self.employee_storage.update(employee)
        self.use_case.calculate_vacation(1)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 4.14)
        saved_time_sheet = self.time_sheet_storage.find_by_id(1)
        self.assertEqual(saved_time_sheet.vacation, -5.86)

        employee = self.employee_storage.find_by_email('with.vacation@email.com')
        employee.employment_date = datetime.today()
        self.employee_storage.update(employee)
        time_sheet = self.time_sheet_storage.find_by_id(1)
        time_sheet.employee_id = 3
        time_sheet.vacation = 0
        self.time_sheet_storage.update(time_sheet)
        self.use_case.calculate_vacation(1)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 3.5)
        saved_time_sheet = self.time_sheet_storage.find_by_id(1)
        self.assertEqual(saved_time_sheet.vacation, -6.5)

    def test_recalculate_vacation(self):
        employee = self.employee_storage.find_by_email('admin@email.com')
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        self.employee_storage.update(employee)
        self.use_case.calculate_vacation(0)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 13.29)
        saved_time_sheet = self.time_sheet_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.vacation, 3.29)

        employee = self.employee_storage.find_by_email('with.vacation@email.com')
        employee.employment_date = datetime(2016, 8, 1)
        self.employee_storage.update(employee)
        time_sheet = self.time_sheet_storage.find_by_id(1)
        time_sheet.employee_id = 3
        time_sheet.vacation = 0
        self.time_sheet_storage.update(time_sheet)
        self.use_case.calculate_vacation(1)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 4.14)
        saved_time_sheet = self.time_sheet_storage.find_by_id(1)
        self.assertEqual(saved_time_sheet.vacation, -5.86)

    def test_calculate_vacation_with_custom_norm(self):
        employee = self.employee_storage.find_by_email("admin@email.com")
        employee.employment_date = datetime(2016, 8, 1)
        employee.vacation = 10
        self.employee_storage.update(employee)
        self.use_case.calculate_vacation(0, 11.5)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 13.29)
        saved_time_sheet = self.time_sheet_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.vacation, 3.29)

        employee = self.employee_storage.find_by_email("with.vacation@email.com")
        employee.employment_date = datetime.today()
        self.employee_storage.update(employee)
        time_sheet = self.time_sheet_storage.find_by_id(0)
        time_sheet.employee_id = 3
        time_sheet.vacation = 0
        self.time_sheet_storage.update(time_sheet)
        self.use_case.calculate_vacation(0, 11.5)

        saved_employee = self.employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 12.3)
        saved_time_sheet = self.time_sheet_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.vacation, 2.3)
