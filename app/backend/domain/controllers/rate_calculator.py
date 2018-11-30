from datetime import datetime


class RateCalculator:
    DATE_OF_START_CALCULATION_RATES = datetime(2016, 8, 31)
    MAX_DAYS = 10
    DAYS_FOR_2_YEARS = 9
    DAYS_FOR_3_YEARS = 8
    MIN_DAYS = 7

    def calculate_rate(self, employment_date, starting_point_date):
        if employment_date <= self.DATE_OF_START_CALCULATION_RATES:
            return self.MIN_DAYS
        delta = starting_point_date - employment_date
        work_years = int(delta.days / 365)
        return self._get_rate(work_years)

    def _get_rate(self, years_working):
        if years_working < 1:
            return self.MAX_DAYS
        elif years_working < 2:
            return self.DAYS_FOR_2_YEARS
        elif years_working < 3:
            return self.DAYS_FOR_3_YEARS
        else:
            return self.MIN_DAYS
