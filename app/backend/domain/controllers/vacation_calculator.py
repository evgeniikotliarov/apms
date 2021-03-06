from functools import reduce

from domain.models.time_sheet import TimeSheet


class VacationCalculator:
    def calculate_vacation(self, time_sheet: TimeSheet, norm=None):
        days_worked = self._calculate_days_worked(time_sheet.sheet)
        vacation = self._calculate_vacation(days_worked, time_sheet.rate)
        using_norm = norm if norm else time_sheet.norm
        used_vacation = self._calculate_used_vacation(days_worked, using_norm)
        time_sheet.vacation = round(vacation - used_vacation, 2)
        return time_sheet

    def calculate_days_worked(self, time_sheet: TimeSheet):
        return self._calculate_days_worked(time_sheet.sheet)

    def calculate_used_vacation(self, time_sheet: TimeSheet):
        days_worked = self._calculate_days_worked(time_sheet.sheet)
        return self._calculate_used_vacation(days_worked, time_sheet.norm)

    @classmethod
    def _calculate_days_worked(cls, sheet):
        return reduce(lambda days_worked, worked_out: days_worked + worked_out, sheet, .0)

    @classmethod
    def _calculate_vacation(cls, days_worked, rate):
        return round(days_worked / rate, 2)

    @classmethod
    def _calculate_used_vacation(cls, days_worked, norm):
        used_days = float(norm - days_worked)
        return used_days if days_worked < norm else .0
