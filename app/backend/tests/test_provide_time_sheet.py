import unittest
from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from exceptions import AccessDeniedToUpdateTimeSheetError
from tests import fixtures


class ProvideTimeSheetTestCase(unittest.TestCase):
    def test_create_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("january"),
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        self.assertIsNotNone(time_sheet)
        self.assertEqual(time_sheet.id, None)
        self.assertEqual(time_sheet.norm, 22)
        self.assertEqual(time_sheet.rate, RateCalculator.DAYS_FOR_3_YEARS)
        self.assertEqual(time_sheet.sheet, fixtures.load("january"))
        self.assertEqual(time_sheet.year, 2018)
        self.assertEqual(time_sheet.month, 1)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertEqual(time_sheet.closed, False)

    def test_create_empty_time_sheet(self):
        time_sheet = TimeSheetProvider.create_empty(date=datetime(2018, 1, 30),
                                                    employee_id=0,
                                                    rate=8)
        self.assertIsNotNone(time_sheet)
        self.assertIsNone(time_sheet.id)
        self.assertEqual(time_sheet.rate, 8)
        self.assertEqual(time_sheet.vacation, 0)
        self.assertEqual(time_sheet.rate, 8)
        self.assertEqual(time_sheet.norm, 23)
        self.assertEqual(time_sheet.sheet.__len__(), 31)
        self.assertEqual(time_sheet.year, 2018)
        self.assertEqual(time_sheet.month, 1)
        self.assertEqual(time_sheet.employee_id, 0)
        self.assertEqual(time_sheet.closed, False)

    def test_create_time_sheet_without_norm(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("january"),
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS
        )
        self.assertIsNotNone(time_sheet)
        self.assertIsNone(time_sheet.norm)

    def test_update_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("january"),
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        time_sheet = TimeSheetProvider.update_with(time_sheet, norm=28)
        self.assertEqual(time_sheet.norm, 28)

        time_sheet = TimeSheetProvider.update_with(time_sheet,
                                                   work_days_sheet=fixtures.load("february"))
        self.assertEqual(time_sheet.sheet, fixtures.load("february"))

    def test_close_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("january"),
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
            norm=22
        )
        time_sheet = TimeSheetProvider.close(time_sheet)
        try:
            TimeSheetProvider.update_with(time_sheet, 10)
            raise Exception("Closed time sheet has been updated")
        except AccessDeniedToUpdateTimeSheetError:
            self.assertEqual(time_sheet.closed, True)

    def test_serialize_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("january"),
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
        self.assertEqual(serialized_time_sheet['sheet'], fixtures.load("january"))

        time_sheet = TimeSheetProvider.close(time_sheet)
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        self.assertEqual(serialized_time_sheet['closed'], True)

    def test_deserialize_time_sheet(self):
        time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 30),
            work_days_sheet=fixtures.load("february"),
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
        self.assertEqual(time_sheet.sheet, fixtures.load("february"))

        time_sheet = TimeSheetProvider.close(time_sheet)
        serialized_time_sheet = TimeSheetProvider.serialize(time_sheet)
        time_sheet = TimeSheetProvider.deserialize(serialized_time_sheet)
        self.assertEqual(time_sheet.closed, True)
