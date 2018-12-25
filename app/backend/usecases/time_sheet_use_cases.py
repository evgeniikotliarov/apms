from datetime import datetime

from domain.controllers.time_sheet_provider import TimeSheetProvider
from exceptions import NotFoundError
from storages.storages import TimeSheetsStorage


class GetTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def get_for_employee(self, employee_id, year, month):
        time_sheet = self.storage.find_first_by(employee_id=employee_id, year=year, month=month)
        return self.controller.serialize(time_sheet)

    def get_by_id(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        return self.controller.serialize(time_sheet)


class GetTimeSheetsUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def get_for_employee(self, employee_id, year=None, month=None):
        if employee_id is None:
            raise NotFoundError()
        if year and month:
            time_sheets = self.storage.find_by(employee_id=employee_id, year=year, month=month)
        elif year:
            time_sheets = self.storage.find_by(employee_id=employee_id, year=year)
        elif month:
            time_sheets = self.storage.find_by(employee_id=employee_id, month=month)
        else:
            time_sheets = self.storage.find_by(employee_id=employee_id)
        return self._serialize_many(time_sheets)

    def get_for_all_employees(self, year=None, month=None):
        if year and month:
            time_sheets = self.storage.find_by(year=year, month=month)
        elif year:
            time_sheets = self.storage.find_by(year=year)
        elif month:
            time_sheets = self.storage.find_by(month=month)
        else:
            time_sheets = self.storage.find_by()
        return self._serialize_many(time_sheets)

    def get_all(self):
        time_sheets = self.storage.get_all()
        return self._serialize_many(time_sheets)

    def _serialize_many(self, time_sheets):
        serialized_time_sheets = []
        for time_sheet in time_sheets:
            serialized_time_sheet = self.controller.serialize(time_sheet)
            serialized_time_sheets.append(serialized_time_sheet)
        return serialized_time_sheets


class CreateTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def create_time_sheet(self, date: datetime, sheet,
                          employee_id: int, rate: int, norm: int = None):
        time_sheet = self.controller.create(date, sheet, employee_id, rate, norm)
        self.storage.save(time_sheet)


class UpdateTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.provider = controller
        self.storage = storage

    def update_day_mark(self, time_sheet_id, day, value):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        sheet = time_sheet.sheet[:]
        sheet[day - 1] = value
        time_sheet.sheet = sheet

        self.storage.update(time_sheet)

    def update_time_sheet(self, time_sheet_id, norm=None, sheet=None):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.provider.update_with(time_sheet, norm, sheet)
        self.storage.update(time_sheet)

    def update_time_sheet_for(self, employee_id, year, month, sheet=None, norm=None):
        try:
            time_sheet = self.storage.find_first_by(employee_id=employee_id, year=year, month=month)
        except NotFoundError:
            date = datetime(year, month, 1)
            time_sheet = self.provider.create_empty(date, employee_id)
        time_sheet = self.provider.update_with(time_sheet, work_days_sheet=sheet, norm=norm)
        self.storage.update(time_sheet)


class CloseTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def close_time_sheet(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.controller.close(time_sheet)
        self.storage.update(time_sheet)
