from datetime import datetime

from domain.exceptions import AccessDeniedToUpdateTimeSheet
from domain.models.time_sheet import TimeSheet


class TimeSheetProvider:
    @staticmethod
    def create(time_sheet_id, date: datetime, work_days_sheet, employee_id, employee_rate, norm=None):
        time_sheet = TimeSheet()
        time_sheet.id = time_sheet_id
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
            raise AccessDeniedToUpdateTimeSheet()
        time_sheet.norm = norm if norm else time_sheet.norm
        time_sheet.sheet = work_days_sheet if work_days_sheet else time_sheet.sheet
        return time_sheet

    @staticmethod
    def close(time_sheet: TimeSheet):
        time_sheet.closed = True
        return time_sheet
