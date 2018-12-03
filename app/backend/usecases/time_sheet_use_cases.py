from datetime import datetime

from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import TimeSheetsStorage


class CreateTimeSheetUseCase:
    def __init__(self, controller: TimeSheetProvider, storage: TimeSheetsStorage):
        self.controller = controller
        self.storage = storage

    def create_time_sheet(self, date: datetime, sheet: dict,
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
