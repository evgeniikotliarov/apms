import unittest
from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.exceptions import AccessDeniedToUpdateTimeSheet


class ProvideTimeSheetTestCase(unittest.TestCase):
    def setUp(self):
        self.sheet = {
            1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0,
            8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 0, 14: 0,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 0, 21: 0,
            22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 0, 28: 0,
            29: 1, 30: 1, 31: 1
        }

    def test_create_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, None)
        self.assertEqual(time_sheet.norm, 22)
        self.assertEqual(time_sheet.rate, RateCalculator.DAYS_FOR_3_YEARS)
        self.assertEqual(time_sheet.sheet, self.sheet)
        self.assertEqual(time_sheet.year, 2018)
        self.assertEqual(time_sheet.month, 1)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertEqual(time_sheet.closed, False)

    def test_create_time_sheet_without_norm(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS
        )
        self.assertIsNotNone(time_sheet)
        self.assertIsNone(time_sheet.norm)

    def test_update_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        time_sheet = TimeSheetProvider.update_with(time_sheet, norm=28)
        self.assertEqual(time_sheet.norm, 28)

        new_sheet = self.sheet.copy()
        new_sheet['1'] = 0
        new_sheet['2'] = 0
        time_sheet = TimeSheetProvider.update_with(time_sheet, work_days_sheet=new_sheet)
        self.assertEqual(time_sheet.sheet, new_sheet)

    def test_close_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        time_sheet = TimeSheetProvider.close(time_sheet)
        try:
            TimeSheetProvider.update_with(time_sheet, 10)
            raise Exception("Closed time sheet has been updated")
        except AccessDeniedToUpdateTimeSheet:
            self.assertEqual(time_sheet.closed, True)

    def test_serialize_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        self.assertEqual(serialized_time_sheet['id'], None)
        self.assertEqual(serialized_time_sheet['year'], 2018)
        self.assertEqual(serialized_time_sheet['month'], 1)
        self.assertEqual(serialized_time_sheet['norm'], 22)
        self.assertEqual(serialized_time_sheet['rate'], RateCalculator.DAYS_FOR_3_YEARS)
        self.assertEqual(serialized_time_sheet['vacation'], None)
        self.assertEqual(serialized_time_sheet['employee_id'], 0)
        self.assertEqual(serialized_time_sheet['closed'], False)
        self.assertEqual(serialized_time_sheet['sheet'], self.sheet)

        time_sheet = TimeSheetProvider.close(time_sheet)
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        self.assertEqual(serialized_time_sheet['closed'], True)

    def test_deserialize_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=self.sheet,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        time_sheet = TimeSheetProvider.deserialize(serialized_time_sheet)
        self.assertEqual(time_sheet.id, None)
        self.assertEqual(time_sheet.year, 2018)
        self.assertEqual(time_sheet.month, 1)
        self.assertEqual(time_sheet.norm, 22)
        self.assertEqual(time_sheet.rate, RateCalculator.DAYS_FOR_3_YEARS)
        self.assertEqual(time_sheet.vacation, None)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertEqual(time_sheet.closed, False)
        self.assertEqual(time_sheet.sheet, self.sheet)

        time_sheet = TimeSheetProvider.close(time_sheet)
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        time_sheet = TimeSheetProvider.deserialize(serialized_time_sheet)
        self.assertEqual(time_sheet.closed, True)
