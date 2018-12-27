import calendar
from datetime import datetime
from functools import reduce


class TimeSheetInitHelper:
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self, date: datetime):
        self.year = date.year
        self.month = date.month

    @property
    def empty_sheet(self):
        count_days_in_month = calendar.monthrange(self.year, self.month)[1]
        return [0 for _ in range(count_days_in_month)]

    @property
    def norm(self):
        return reduce(lambda norm, day: norm + (1 if not self.__is_weekend(day) else 0),
                      self.__get_days_in_month())

    def calculate_norm_for_day(self, target_day):
        return reduce(lambda norm, day: norm + (1 if not self.__is_weekend(day) else 0),
                      range(1, target_day + 1))

    def __is_weekend(self, day):
        day_of_week = datetime(self.year, self.month, day).weekday()
        return day_of_week in [self.SATURDAY, self.SUNDAY]

    def __get_days_in_month(self):
        count_days_in_month = calendar.monthrange(self.year, self.month)[1]
        return range(1, count_days_in_month + 1)
