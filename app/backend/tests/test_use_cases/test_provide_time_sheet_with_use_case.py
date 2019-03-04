import unittest
from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from exceptions import NotFoundError
from storages.storages import TimeSheetsStorage, EmployeesStorage
from tests import fixtures
from tests.fake_db import FakeDb
from usecases.employee_use_cases import GetEmployeeUseCase
from usecases.time_sheet_use_cases import CreateTimeSheetUseCase, UpdateTimeSheetUseCase, \
    CloseTimeSheetUseCase, GetTimeSheetUseCase, GetTimeSheetsUseCase


class TestTimeSheetEmployeeUseCase(unittest.TestCase):
    def test_get_time_sheet(self):
        ts_storage = TimeSheetsStorage(FakeDb().build())
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        ts_provider = TimeSheetProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        use_case = GetTimeSheetUseCase(ts_provider, e_use_case, ts_storage)

        time_sheet = use_case.get_for_employee(employee_id=0, year=2019, month=1)
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheet = use_case.get_by_id(time_sheet_id=0)
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

    def test_get_not_exist_time_sheet(self):
        ts_storage = TimeSheetsStorage(FakeDb().build())
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        ts_provider = TimeSheetProvider()
        use_case = GetTimeSheetUseCase(ts_provider, e_use_case, ts_storage)

        time_sheet = use_case.get_for_employee(employee_id=0, year=2019, month=12)
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 12)
        self.assertEqual(time_sheet['sheet'].__len__(), 31)
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 22)

    def test_get_time_sheets(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        use_case = GetTimeSheetsUseCase(controller, e_use_case, storage)

        time_sheets = use_case.get_for_employee(employee_id=0, year=2019, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0, year=2019)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(year=2019)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(year=2019, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_all()
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2019)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

    def test_create_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = CreateTimeSheetUseCase(controller, storage)

        now = datetime(2019, 2, 1)
        use_case.create_time_sheet(now, fixtures.load('january'), 0, 10, 10)
        saved_time_sheet = storage.find_by_id(2)
        self.assertEqual(saved_time_sheet.year, 2019)
        self.assertEqual(saved_time_sheet.month, 2)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('january'))
        self.assertEqual(saved_time_sheet.employee_id, 0)
        self.assertEqual(saved_time_sheet.rate, 10)
        self.assertEqual(saved_time_sheet.norm, 10)

    def test_update_one_day(self):
        ts_storage = TimeSheetsStorage(FakeDb().build())
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        ts_provider = TimeSheetProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        calculator = VacationCalculator()
        use_case = UpdateTimeSheetUseCase(ts_provider, e_use_case, calculator, ts_storage)

        use_case.update_day_mark(0, 1, 0.5)

        saved_time_sheet = ts_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.sheet[0], 0.5)
        self.assertNotEqual(saved_time_sheet.vacation, 1.0)

    def test_update_time_sheet(self):
        ts_storage = TimeSheetsStorage(FakeDb().build())
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        ts_provider = TimeSheetProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        calculator = VacationCalculator()
        use_case = UpdateTimeSheetUseCase(ts_provider, e_use_case, calculator, ts_storage)

        use_case.update_time_sheet(0, sheet=fixtures.load('february'), norm=19)

        saved_time_sheet = ts_storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.id, 0)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('february'))
        self.assertEqual(saved_time_sheet.norm, 19)
        self.assertNotEqual(saved_time_sheet.vacation, 1.0)

        use_case.update_time_sheet_for(0, 2019, 1, sheet=fixtures.load('full_january'))

        saved_time_sheet = ts_storage.find_first_by(employee_id=0, year=2019, month=1)
        self.assertEqual(saved_time_sheet.employee_id, 0)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('full_january'))
        self.assertEqual(saved_time_sheet.norm, 19)
        self.assertNotEqual(saved_time_sheet.vacation, 1.0)

    def test_update_time_sheet_for_not_exist(self):
        ts_storage = TimeSheetsStorage(FakeDb().build())
        e_storage = EmployeesStorage(FakeDb().build())
        e_provider = EmployeeProvider()
        ts_provider = TimeSheetProvider()
        e_use_case = GetEmployeeUseCase(e_provider, e_storage)
        calculator = VacationCalculator()
        use_case = UpdateTimeSheetUseCase(ts_provider, e_use_case, calculator, ts_storage)
        try:
            ts_storage.find_first_by(employee_id=3, year=2019, month=5)
            raise Exception('Time sheet should not exist')
        except NotFoundError:
            pass
        use_case.update_time_sheet_for(employee_id=3,
                                       year=2019,
                                       month=5,
                                       sheet=fixtures.load('february'))

        saved_time_sheet = ts_storage.find_first_by(employee_id=3, year=2019, month=5)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('february'))

    def test_close_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = CloseTimeSheetUseCase(controller, storage)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.closed, False)
        use_case.close_time_sheet(0)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.id, 0)
        self.assertEqual(saved_time_sheet.closed, True)
