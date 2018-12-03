import unittest

from domain.controllers.employee_provider import EmployeeProvider
from storages.storages import EmployeesStorage
# noinspection PyPackageRequirements
from tests.fake_db import FakeEmployeesDb


class TestProvideEmployeeUseCase(unittest.TestCase):
    def test_update_employees_vacation(self):
        employee_storage = EmployeesStorage(FakeEmployeesDb())
        time_sheet_storage = TimeSheetStorage(FakeTimeSheetDb())
        employee_controller = EmployeeProvider()
        time_sheet_controller = EmployeeProvider()
        use_case = CalculateVacationUseCase(employee_controller, time_sheet_controller,
                                            employee_storage, time_sheet_storage)

        saved_employee = employee_storage.find_by_id(0)
        self.assertEqual(saved_employee.is_admin(), False)
