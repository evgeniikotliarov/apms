from datetime import datetime

from exceptions import AccessDeniedToUpdateTimeSheetError
from domain.models.time_sheet import TimeSheet


class TimeSheetProvider:
    @staticmethod
    def create(date: datetime, work_days_sheet, employee_id, employee_rate, norm=None):
        time_sheet = TimeSheet()
        time_sheet.norm = norm
        time_sheet.employee_rate = employee_rate
        time_sheet.year = date.year
        time_sheet.month = date.month
        time_sheet.sheet = work_days_sheet
        time_sheet.employee_id = employee_id
        time_sheet.closed = False
        return time_sheet

    @staticmethod
    def update_with(time_sheet: TimeSheet, norm=None, work_days_sheet=None):
        if time_sheet.closed:
            raise AccessDeniedToUpdateTimeSheetError()
        time_sheet.norm = norm if norm else time_sheet.norm
        time_sheet.sheet = work_days_sheet if work_days_sheet else time_sheet.sheet
        return time_sheet

    @staticmethod
    def close(time_sheet: TimeSheet):
        time_sheet.closed = True
        return time_sheet

    @classmethod
    def serialize(cls, time_sheet: TimeSheet):
        return time_sheet.__dict__

    @classmethod
    def deserialize(cls, serialized_time_sheet: dict):
        time_sheet = TimeSheet()
        for key, value in serialized_time_sheet.items():
            setattr(time_sheet, key, value)
        return time_sheet
