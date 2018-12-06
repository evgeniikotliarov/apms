import unittest
from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
# noinspection PyPackageRequirements
from tests.fixtures.sheets import january, february, half_january, compensation_january, \
    full_january, compensation_january_with_half_day


class TestRateCalculator(unittest.TestCase):
    def setUp(self):
        self.january_time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 1, 31),
            work_days_sheet=january,
            employee_id=0,
            employee_rate=RateCalculator.DAYS_FOR_3_YEARS,
        )
        self.february_time_sheet = TimeSheetProvider.create(
            date=datetime(2018, 2, 28),
            work_days_sheet=february,
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
        time_sheet.sheet = half_january
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
        time_sheet.sheet = compensation_january
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

    def test_calculate_with_compensation_half_days_sheet(self):
        time_sheet = self.january_time_sheet
        time_sheet.sheet = compensation_january_with_half_day
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
        time_sheet.sheet = full_january
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
