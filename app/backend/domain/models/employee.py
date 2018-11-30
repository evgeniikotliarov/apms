from datetime import datetime

from backend.domain.controllers.rate_calculator import RateCalculator


class Employee:
    def __init__(self):
        self.id = None
        self.name = None
        self.email = None
        self.password = None
        self.activated = None
        self.vacation = None
        self.employment_date = None

    @property
    def rate(self):
        calculator = RateCalculator()
        return calculator.calculate_rate(
            employment_date=self.employment_date,
            starting_point_date=datetime.now()
        )