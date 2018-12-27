import unittest
from datetime import datetime

from domain.controllers.time_sheet_initializer import TimeSheetInitHelper
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.models.time_sheet import TimeSheet


class TestSheetInitializer(unittest.TestCase):
    def test_calculate_norm(self):
        time_sheet = TimeSheet()

        initializer = TimeSheetInitHelper(datetime(2018, 1, 1))
        time_sheet.sheet = initializer.empty_sheet
        time_sheet.norm = initializer.norm
        self.assertEqual(time_sheet.norm, 23)
        self.assertEqual(time_sheet.sheet.__len__(), 31)

        initializer = TimeSheetInitHelper(datetime(2018, 2, 1))
        time_sheet.sheet = initializer.empty_sheet
        time_sheet.norm = initializer.norm
        self.assertEqual(time_sheet.norm, 20)
        self.assertEqual(time_sheet.sheet.__len__(), 28)

        time_sheet = TimeSheetProvider.update_with(time_sheet, norm=17)
        self.assertEqual(time_sheet.norm, 17)

    def test_calculate_norm_for_day(self):
        time_sheet = TimeSheet()

        initializer = TimeSheetInitHelper(datetime(2018, 1, 1))
        time_sheet.sheet = initializer.empty_sheet
        time_sheet.norm = initializer.calculate_norm_for_day(16)
        self.assertEqual(time_sheet.norm, 12)
        self.assertEqual(time_sheet.sheet.__len__(), 31)
