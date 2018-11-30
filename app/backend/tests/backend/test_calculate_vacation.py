import unittest
from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator


class TestRateCalculator(unittest.TestCase):
    def setUp(self):
        self.full_january = {
            1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
            8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1,
            22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1,
            29: 1, 30: 1, 31: 1
        }
        self.compensation_january = {
            1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 1,
            8: 0, 9: 1, 10: 1, 11: 1, 12: 1, 13: 0, 14: 1,
            15: 0, 16: 1, 17: 1, 18: 1, 19: 1, 20: 0, 21: 1,
            22: 0, 23: 1, 24: 1, 25: 1, 26: 1, 27: 0, 28: 1,
            29: 1, 30: 1, 31: 1
        }
        self.half_january = {
            1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0,
            8: 1, 9: 1, 10: 1, 11: 0, 12: 0, 13: 0, 14: 0,
            15: 1, 16: 1, 17: 1, 18: 0, 19: 0, 20: 0, 21: 0,
            22: 1, 23: 1, 24: 1, 25: 0, 26: 0, 27: 0, 28: 0,
            29: 1, 30: 1, 31: 1
        }
        self.january = {
            1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0,
            8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 0, 14: 0,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 0, 21: 0,
            22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 0, 28: 0,
            29: 1, 30: 1, 31: 1
        }
        self.february = {
            1: 1, 2: 1, 3: 0, 4: 0,
            5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0, 11: 0,
            12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 0, 18: 0,
            19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 0, 25: 0,
            26: 1, 27: 1, 28: 1
        }
        self.january_time_sheet = TimeSheetProvider.create(
            time_sheet_id=0,
            date=datetime(2018, 1, 31),
            work_days_sheet=self.january,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
        )
        self.february_time_sheet = TimeSheetProvider.create(
            time_sheet_id=1,
            date=datetime(2018, 2, 28),
            work_days_sheet=self.february,
            employee_id=0,
            employee_rate=RateCalculator.MAX_DAYS,
        )

    def test_calculate_norm(self):
        calculator = VacationCalculator()
        time_sheet = calculator.calculate_norm(self.january_time_sheet)
        self.assertEqual(time_sheet.norm, 23)

        calculator = VacationCalculator()
        time_sheet = calculator.calculate_norm(self.february_time_sheet)
        self.assertEqual(time_sheet.norm, 20)

        time_sheet = TimeSheetProvider.update_with(time_sheet, norm=17)
        self.assertEqual(time_sheet.norm, 17)

    def test_calculate_with_full_time_sheet(self):
        time_sheet = self.january_time_sheet
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_norm(time_sheet)
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)

    def test_calculate_with_half_time_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = self.half_january
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, -5.86)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.12)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.33)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.5)

    def test_calculate_with_compensation_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = self.compensation_january
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_norm(time_sheet)
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)

    def test_calculate_with_full_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = self.full_january
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_norm(time_sheet)
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 4.43)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.44)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation_with_auto_norm(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.1)
