import calendar
from datetime import datetime
from functools import reduce

from domain.models.time_sheet import TimeSheet


class VacationCalculator:
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self):
        self.month = None
        self.year = None

    def calculate_vacation(self, time_sheet: TimeSheet):
        self.__init_date(time_sheet)
        days_worked = self._calculate_days_worked(time_sheet.sheet)
        vacation = self._calculate_vacation(days_worked, time_sheet.rate)
        used_vacation = self._calculate_used_vacation(days_worked, time_sheet.norm)
        time_sheet.vacation = round(vacation - used_vacation, 2)
        return time_sheet

    def calculate_vacation_with_auto_norm(self, time_sheet: TimeSheet):
        time_sheet = self.calculate_norm(time_sheet)
        return self.calculate_vacation(time_sheet)

    def calculate_norm(self, time_sheet: TimeSheet):
        self.__init_date(time_sheet)
        time_sheet.norm = reduce(lambda norm, day: norm + (1 if not self.__is_weekend(day) else 0),
                                 self.__get_days_in_month())
        return time_sheet

    @classmethod
    def _calculate_days_worked(cls, sheet):
        return reduce(lambda days_worked, day: days_worked + sheet[day], sheet, .0)

    @classmethod
    def _calculate_vacation(cls, days_worked, rate):
        return round(days_worked / rate, 2)

    @classmethod
    def _calculate_used_vacation(cls, days_worked, norm):
        return float(norm - days_worked) if days_worked < norm else 0.

    def __init_date(self, time_sheet: TimeSheet):
        self.month = time_sheet.month
        self.year = time_sheet.year

    def __is_weekend(self, day):
        day_of_week = datetime(self.year, self.month, day).weekday()
        return day_of_week in [self.SATURDAY, self.SUNDAY]

    def __get_days_in_month(self):
        count_days_in_month = calendar.monthrange(self.year, self.month)[1]
        return range(1, count_days_in_month + 1)
