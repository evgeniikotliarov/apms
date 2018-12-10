from datetime import datetime

from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import TimeSheetsStorage


class GetTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def get_for_employee(self, employee_id, year, month):
        time_sheet = self.storage.find_by(employee_id=employee_id, year=year, month=month)[0]
        return self.controller.serialize(time_sheet)

    def get_by_id(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        return self.controller.serialize(time_sheet)


class GetAllTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def get_for_employee(self, employee_id, year=None, month=None):
        if employee_id and year and month:
            time_sheets = self.storage.find_by(employee_id=employee_id, year=year, month=month)
        elif employee_id and year:
            time_sheets = self.storage.find_by(employee_id=employee_id, year=year)
        elif employee_id and month:
            time_sheets = self.storage.find_by(employee_id=employee_id, month=month)
        else:
            time_sheets = self.storage.find_by(employee_id=employee_id)
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
                          employee_id: int, rate: int, norm: int=None):
        time_sheet = self.controller.create(date, sheet, employee_id, rate, norm)
        self.storage.save(time_sheet)


class UpdateTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def update_time_sheet(self, time_sheet_id, norm=None, sheet=None):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.controller.update_with(time_sheet, norm, sheet)
        self.storage.update(time_sheet)


class CloseTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def close_time_sheet(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.controller.close(time_sheet)
        self.storage.update(time_sheet)
