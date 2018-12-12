import unittest
from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import TimeSheetsStorage
from tests.fake_db import FakeDb


class TestTimeSheetStorage(unittest.TestCase):
    def test_get_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        time_sheet = storage.find_by_id(0)
        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, 0)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertIsNotNone(time_sheet.year)
        self.assertIsNotNone(time_sheet.month)
        self.assertIsNotNone(time_sheet.sheet)
        self.assertIsNotNone(time_sheet.rate)
        self.assertIsNotNone(time_sheet.norm)
        self.assertIsNotNone(time_sheet.closed)

    def test_get_first_by_filter_time_sheet(self):
        storage = TimeSheetsStorage(FakeDb().build())
        time_sheet = storage.find_first_by(id=0)
        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, 0)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertIsNotNone(time_sheet.year)
        self.assertIsNotNone(time_sheet.month)
        self.assertIsNotNone(time_sheet.sheet)
        self.assertIsNotNone(time_sheet.rate)
        self.assertIsNotNone(time_sheet.norm)
        self.assertIsNotNone(time_sheet.closed)

    def test_get_all_employee(self):
        storage = TimeSheetsStorage(FakeDb().build())
        employees = storage.get_all()
        self.assertIsNotNone(employees)
        time_sheet = employees[0]
        self.assertEqual(time_sheet.id, 0)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertIsNotNone(time_sheet.year)
        self.assertIsNotNone(time_sheet.month)
        self.assertIsNotNone(time_sheet.sheet)
        self.assertIsNotNone(time_sheet.rate)
        self.assertIsNotNone(time_sheet.norm)
        self.assertIsNotNone(time_sheet.closed)

    def test_save_employees(self):
        storage = TimeSheetsStorage(FakeDb().build())
        first_time_sheet = storage.find_by_id(0)
        date = datetime(2018, 2, 1)
        time_sheet = TimeSheetProvider.create(date, first_time_sheet.sheet,
                                              5, RateCalculator.MAX_DAYS, norm=10)
        time_sheet.id = 75
        storage.save(time_sheet)

        time_sheet = storage.find_by_id(75)
        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, 75)
        self.assertEqual(time_sheet.year, 2018)
        self.assertEqual(time_sheet.month, 2)
        self.assertEqual(time_sheet.sheet, first_time_sheet.sheet)
        self.assertEqual(time_sheet.employee_id, 5)
        self.assertEqual(time_sheet.rate, RateCalculator.MAX_DAYS)
        self.assertEqual(time_sheet.norm, 10)

    def test_update_employee(self):
        storage = TimeSheetsStorage(FakeDb().build())
        time_sheet = storage.find_by_id(0)
        time_sheet.norm = 23
        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        storage.update(time_sheet)

        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, 0)
        self.assertEqual(time_sheet.norm, 23)
        self.assertEqual(time_sheet.rate, RateCalculator.DAYS_FOR_2_YEARS)
