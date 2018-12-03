import unittest
from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage
# noinspection PyPackageRequirements
from tests.fake_db import FakeEmployeesDb, FakeTimeSheetsDb
from tests.fixtures.sheets import january, half_january
from usecases.calculate_vacation_use_case import CalculateVacationUseCase


class TestProvideEmployeeUseCase(unittest.TestCase):
    def test_calculate_vacation(self):
        employee_storage = EmployeesStorage(FakeEmployeesDb())
        time_sheet_storage = TimeSheetsStorage(FakeTimeSheetsDb())
        employee_controller = EmployeeProvider()
        time_sheet_controller = TimeSheetProvider()
        calculator = VacationCalculator()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller, calculator,
                                            employee_storage, time_sheet_storage)
        employee = employee_storage.find_by_id(0)
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        use_case.calculate_vacation(0, january, datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_id(0)
        self.assertEqual(saved_employee.vacation, 13.29)

        employee.vacation = 10
        employee.employment_date = datetime(2017, 12, 1)
        use_case.calculate_vacation(0, january, datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_id(0)
        self.assertEqual(saved_employee.vacation, 12.3)

    def test_calculate_vacation_with_minus(self):
        employee_storage = EmployeesStorage(FakeEmployeesDb())
        time_sheet_storage = TimeSheetsStorage(FakeTimeSheetsDb())
        employee_controller = EmployeeProvider()
        time_sheet_controller = TimeSheetProvider()
        calculator = VacationCalculator()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller, calculator,
                                            employee_storage, time_sheet_storage)
        employee = employee_storage.find_by_id(0)
        employee.vacation = 10
        employee.employment_date = datetime(2016, 8, 1)
        use_case.calculate_vacation(0, half_january, datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_id(0)
        self.assertEqual(saved_employee.vacation, 4.14)

        employee.vacation = 10
        employee.employment_date = datetime(2017, 12, 1)
        use_case.calculate_vacation(0, half_january, datetime(2018, 1, 1))
        saved_employee = employee_storage.find_by_id(0)
        self.assertEqual(saved_employee.vacation, 3.5)
