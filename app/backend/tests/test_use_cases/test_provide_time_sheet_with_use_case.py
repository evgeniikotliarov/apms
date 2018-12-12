import unittest
from datetime import datetime

from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import TimeSheetsStorage
from tests import fixtures
from tests.fake_db import FakeDb
from usecases.time_sheet_use_cases import CreateTimeSheetUseCase, UpdateTimeSheetUseCase, \
    CloseTimeSheetUseCase, GetTimeSheetUseCase, GetTimeSheetsUseCase


class TestTimeSheetEmployeeUseCase(unittest.TestCase):
    def test_get_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = GetTimeSheetUseCase(controller, storage)

        time_sheet = use_case.get_for_employee(employee_id=0, year=2018, month=1)
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheet = use_case.get_by_id(time_sheet_id=0)
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

    def test_get_time_sheets(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = GetTimeSheetsUseCase(controller, storage)

        time_sheets = use_case.get_for_employee(employee_id=0, year=2018, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0, year=2018)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(year=2018)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(year=2018, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_all_employees(month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0, month=1)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_for_employee(employee_id=0)
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

        time_sheets = use_case.get_all()
        time_sheet = time_sheets[0]
        self.assertEqual(time_sheet['year'], 2018)
        self.assertEqual(time_sheet['month'], 1)
        self.assertEqual(time_sheet['sheet'], fixtures.load('january'))
        self.assertEqual(time_sheet['employee_id'], 0)
        self.assertEqual(time_sheet['rate'], 10)
        self.assertEqual(time_sheet['norm'], 23)

    def test_create_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = CreateTimeSheetUseCase(controller, storage)

        now = datetime(2018, 2, 1)
        use_case.create_time_sheet(now, fixtures.load('january'), 0, 10, 10)
        saved_time_sheet = storage.find_by_id(2)
        self.assertEqual(saved_time_sheet.year, 2018)
        self.assertEqual(saved_time_sheet.month, 2)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('january'))
        self.assertEqual(saved_time_sheet.employee_id, 0)
        self.assertEqual(saved_time_sheet.rate, 10)
        self.assertEqual(saved_time_sheet.norm, 10)

    def test_update_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        controller = TimeSheetProvider()
        use_case = UpdateTimeSheetUseCase(controller, storage)

        use_case.update_time_sheet(0, sheet=fixtures.load('february'), norm=19)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.id, 0)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('february'))
        self.assertEqual(saved_time_sheet.norm, 19)

        use_case.update_time_sheet_for(0, 2018, 1, sheet=fixtures.load('full_january'))

        saved_time_sheet = storage.find_by(employee_id=0, year=2018, month=1)[0]
        self.assertEqual(saved_time_sheet.employee_id, 0)
        self.assertEqual(saved_time_sheet.sheet, fixtures.load('full_january'))
        self.assertEqual(saved_time_sheet.norm, 19)

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
