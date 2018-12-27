import unittest

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.vacation_calculator import VacationCalculator
from domain.models.time_sheet import TimeSheet
from tests import fixtures


class TestRateCalculator(unittest.TestCase):
    def setUp(self):
        self.january_time_sheet = fixtures.load_instance('january_time_sheet', TimeSheet)
        self.february_time_sheet = fixtures.load_instance('february_time_sheet', TimeSheet)

    def test_calculate_with_half_time_sheet_for_day(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = fixtures.load("half_january")
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet, 12)
        self.assertEqual(time_sheet.vacation, 2.14)
        self.assertEqual(time_sheet.norm, 23)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet, 12)
        self.assertEqual(time_sheet.vacation, 1.88)
        self.assertEqual(time_sheet.norm, 23)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet, 12)
        self.assertEqual(time_sheet.vacation, 1.67)
        self.assertEqual(time_sheet.norm, 23)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet, 12)
        self.assertEqual(time_sheet.vacation, 1.5)
        self.assertEqual(time_sheet.norm, 23)

    def test_calculate_with_full_time_sheet(self):
        time_sheet = self.january_time_sheet
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)

    def test_calculate_with_half_time_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = fixtures.load("half_january")
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, -5.86)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.12)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.33)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, -6.5)

    def test_calculate_with_compensation_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = fixtures.load("compensation_january")
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)

    def test_calculate_with_compensation_half_days_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = fixtures.load("compensation_january_with_half_day")
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)

    def test_calculate_with_full_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = fixtures.load("full_january")
        calculator = VacationCalculator()

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 4.43)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.44)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.1)

    def test_calculate_with_custom_norm(self):
        time_sheet = self.january_time_sheet
        calculator = VacationCalculator()
        time_sheet.norm = 10

        time_sheet.rate = RateCalculator.MIN_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 3.29)

        time_sheet.rate = RateCalculator.DAYS_FOR_3_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.88)

        time_sheet.rate = RateCalculator.DAYS_FOR_2_YEARS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.56)

        time_sheet.rate = RateCalculator.MAX_DAYS
        time_sheet = calculator.calculate_vacation(time_sheet)
        self.assertEqual(time_sheet.vacation, 2.3)
