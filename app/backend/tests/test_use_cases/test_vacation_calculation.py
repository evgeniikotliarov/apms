import unittest
from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage
from tests import fixtures
from tests.fake_db import FakeDb
from usecases.calculate_vacation_use_case import CalculateVacationUseCase


class TestProvideEmployeeUseCase(unittest.TestCase):
    def test_calculate_vacation(self):
        db = FakeDb().build()
        employee_storage = EmployeesStorage(db)
        time_sheet_storage = TimeSheetsStorage(db)
        employee_controller = EmployeeProvider()
        time_sheet_controller = TimeSheetProvider()
        calculator = VacationCalculator()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller, calculator,
                                            employee_storage, time_sheet_storage)

        employee = employee_storage.find_by_email("admin@email.com")
        employee.employment_date = datetime(2016, 8, 1)
        employee.vacation = 10
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 13.29)

        employee = employee_storage.find_by_email("with.vacation@email.com")
        employee.employment_date = datetime(2017, 12, 1)
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 12.3)

    def test_calculate_vacation_with_minus(self):
        db = FakeDb().build()
        employee_storage = EmployeesStorage(db)
        time_sheet_storage = TimeSheetsStorage(db)
        employee_controller = EmployeeProvider()
        time_sheet_controller = TimeSheetProvider()
        calculator = VacationCalculator()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller, calculator,
                                            employee_storage, time_sheet_storage)
        employee = employee_storage.find_by_email('admin@email.com')
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('half_january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 4.14)

        employee = employee_storage.find_by_email('with.vacation@email.com')
        employee.employment_date = datetime(2017, 12, 1)
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('half_january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 3.5)

    def test_recalculate_vacation(self):
        employee_storage = EmployeesStorage(FakeDb().build())
        time_sheet_storage = TimeSheetsStorage(FakeDb().build())
        employee_controller = EmployeeProvider()
        time_sheet_controller = TimeSheetProvider()
        calculator = VacationCalculator()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller, calculator,
                                            employee_storage, time_sheet_storage)
        employee = employee_storage.find_by_email('admin@email.com')
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 13.29)

        employee = employee_storage.find_by_email('with.vacation@email.com')
        employee.employment_date = datetime(2016, 8, 1)
        employee_storage.update(employee)
        use_case.calculate_vacation(employee.id, fixtures.load('half_january'), datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_email(employee.email)
        self.assertEqual(saved_employee.vacation, 4.14)
