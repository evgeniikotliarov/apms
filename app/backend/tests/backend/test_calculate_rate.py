import unittest
from datetime import datetime

from backend.domain.controllers.rate_calculator import RateCalculator


class TestRateCalculator(unittest.TestCase):
    def test_calculation_rate_10(self):
        calc = RateCalculator()

        register_date = datetime(2018, 1, 10)
        actual_rate = calc.calculate_rate(register_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 10)

        register_date = datetime(2017, 10, 15)
        actual_rate = calc.calculate_rate(register_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 10)

        register_date = datetime(2017, 2, 15)
        actual_rate = calc.calculate_rate(register_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 10)

    def test_calculation_rate_9(self):
        calc = RateCalculator()

        some_date = datetime(2016, 9, 1)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 9)

        some_date = datetime(2016, 9, 1)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 8, 31))
        self.assertEqual(actual_rate, 9)

        some_date = datetime(2016, 9, 1)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 9)

    def test_calculation_rate_8(self):
        calc = RateCalculator()

        some_date = datetime(2016, 9, 15)
        actual_rate = calc.calculate_rate(some_date, datetime(2019, 9, 5))
        self.assertEqual(actual_rate, 8)

        some_date = datetime(2016, 9, 1)
        actual_rate = calc.calculate_rate(some_date, datetime(2019, 1, 1))
        self.assertEqual(actual_rate, 8)

        some_date = datetime(2016, 9, 1)
        actual_rate = calc.calculate_rate(some_date, datetime(2019, 8, 31))
        self.assertEqual(actual_rate, 8)

    def test_calculation_rate_7(self):
        calc = RateCalculator()

        some_date = datetime(2016, 8, 30)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 7)

        some_date = datetime(2016, 8, 31)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 7)

        some_date = datetime(2015, 2, 25)
        actual_rate = calc.calculate_rate(some_date, datetime(2018, 1, 15))
        self.assertEqual(actual_rate, 7)

if __name__ == '__main__':
    unittest.main()
