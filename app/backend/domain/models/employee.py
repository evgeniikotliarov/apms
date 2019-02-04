from datetime import datetime

from domain.controllers.rate_calculator import RateCalculator


class Employee:
    def __init__(self):
        self.id = None
        self.name = None
        self.email = None
        self.password = None
        self.vacation = None
        self.is_admin = None
        self.activated = None
        self.employment_date = None
        self.acceptance_date = None

    @property
    def rate(self):
        if not self.employment_date:
            return 0
        calculator = RateCalculator()
        return calculator.calculate_rate(
            employment_date=self.employment_date,
            starting_point_date=datetime.now())
