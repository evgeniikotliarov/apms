import unittest
from datetime import datetime

from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import TimeSheetsStorage
# noinspection PyPackageRequirements
from tests.fake_db import FakeTimeSheetsDb
# noinspection PyPackageRequirements
from tests.fixtures.sheets import january, february
from usecases.time_sheet_use_cases import CreateTimeSheetUseCase, UpdateTimeSheetUseCase, \
    CloseTimeSheetUseCase


class TestTimeSheetEmployeeUseCase(unittest.TestCase):
    def test_create_time_sheet(self):
        storage = TimeSheetsStorage(FakeTimeSheetsDb())
        controller = TimeSheetProvider()
        use_case = CreateTimeSheetUseCase(controller, storage)

        now = datetime(2018, 2, 1)
        use_case.create_time_sheet(now, january, 0, 10, 10)
        saved_time_sheet = storage.find_by_id(1)
        self.assertEqual(saved_time_sheet.year, 2018)
        self.assertEqual(saved_time_sheet.month, 2)
        self.assertEqual(saved_time_sheet.sheet, january)
        self.assertEqual(saved_time_sheet.employee_id, 0)
        self.assertEqual(saved_time_sheet.rate, 10)
        self.assertEqual(saved_time_sheet.norm, 10)

    def test_update_time_sheet(self):
        storage = TimeSheetsStorage(FakeTimeSheetsDb())
        controller = TimeSheetProvider()
        use_case = UpdateTimeSheetUseCase(controller, storage)

        use_case.update_time_sheet(0, sheet=february, norm=19)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.id, 0)
        self.assertEqual(saved_time_sheet.sheet, february)
        self.assertEqual(saved_time_sheet.norm, 19)

    def test_close_time_sheet(self):
        storage = TimeSheetsStorage(FakeTimeSheetsDb())
        controller = TimeSheetProvider()
        use_case = CloseTimeSheetUseCase(controller, storage)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.closed, False)
        use_case.close_time_sheet(0)

        saved_time_sheet = storage.find_by_id(0)
        self.assertEqual(saved_time_sheet.id, 0)
        self.assertEqual(saved_time_sheet.closed, True)
