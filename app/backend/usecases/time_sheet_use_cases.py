from datetime import datetime

from domain.controllers.time_sheet_initializer import TimeSheetInitHelper
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from exceptions import NotFoundError
from storages.storages import TimeSheetsStorage
from usecases.employee_use_cases import GetEmployeeUseCase


class GetTimeSheetUseCase:
    def __init__(self,
                 time_sheet_provider: TimeSheetProvider,
                 employee_use_case: GetEmployeeUseCase,
                 storage: TimeSheetsStorage):
        self.time_sheet_provider = time_sheet_provider
        self.employee_use_case = employee_use_case
        self.storage = storage

    def get_for_employee(self, employee_id, year, month):
        time_sheet = _get_or_create(use_case=self, year=year, month=month, employee_id=employee_id)
        time_sheet = self.time_sheet_provider.serialize(time_sheet)
        return time_sheet

    def get_by_id(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        return self.time_sheet_provider.serialize(time_sheet)


class GetTimeSheetsUseCase:
    def __init__(self,
                 time_sheet_provider: TimeSheetProvider,
                 employee_use_case: GetEmployeeUseCase,
                 storage: TimeSheetsStorage):
        self.time_sheet_provider = time_sheet_provider
        self.employee_use_case = employee_use_case
        self.storage = storage

    def get_for_employee(self, employee_id, year=None, month=None):
        if employee_id is None:
            raise NotFoundError()
        if year and month:
            time_sheet = _get_or_create(
                use_case=self,
                year=year,
                month=month,
                employee_id=employee_id)
            return [self.time_sheet_provider.serialize(time_sheet)]
        elif year:
            time_sheets = self.storage.find_by(employee_id=employee_id, year=year)
        elif month:
            time_sheets = self.storage.find_by(employee_id=employee_id, month=month)
        else:
            time_sheets = self.storage.find_by(employee_id=employee_id)
        return self._serialize_many(time_sheets)

    def get_for_all_employees(self, year=None, month=None):
        if year and month:
            return self._get_or_create_for_all(year, month)
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
            serialized_time_sheet = self.time_sheet_provider.serialize(time_sheet)
            serialized_time_sheets.append(serialized_time_sheet)
        return serialized_time_sheets

    def _get_or_create_for_all(self, year, month):
        time_sheets = []
        for employee in self.employee_use_case.storage.find_by(activated=True):
            time_sheets.append(_get_or_create(self, year, month, employee.id))
        return self._serialize_many(time_sheets)


class CreateTimeSheetUseCase:
    def __init__(self, provider: TimeSheetProvider, storage: TimeSheetsStorage):
        self.provider = provider
        self.storage = storage

    def create_time_sheet(self, date: datetime, sheet,
                          employee_id: int, rate: int, norm: int = None):
        time_sheet = self.provider.create(date, sheet, employee_id, rate, norm)
        self.storage.save(time_sheet)


class UpdateTimeSheetUseCase:
    def __init__(self,
                 time_sheet_provider: TimeSheetProvider,
                 employee_use_case: GetEmployeeUseCase,
                 calculator: VacationCalculator,
                 storage: TimeSheetsStorage):
        self.time_sheet_provider = time_sheet_provider
        self.employee_use_case = employee_use_case
        self.calculator = calculator
        self.storage = storage

    def update_day_mark(self, time_sheet_id, day, value):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        sheet = time_sheet.sheet[:]
        sheet[day - 1] = value
        time_sheet.sheet = sheet
        now = datetime.now()
        if time_sheet.month == now.month:
            norm = self._calculate_norm_for_day(time_sheet, now.day)
        else:
            norm = time_sheet.norm
        time_sheet = self.calculator.calculate_vacation(time_sheet, norm)
        self.storage.update(time_sheet)

    def update_time_sheet(self, time_sheet_id, norm=None, sheet=None):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.time_sheet_provider.update_with(time_sheet, norm, sheet)
        time_sheet = self.calculator.calculate_vacation(time_sheet)
        self.storage.update(time_sheet)

    def update_time_sheet_for(self, employee_id, year, month, sheet=None, norm=None):
        time_sheet = _get_or_create(
            use_case=self,
            year=year,
            month=month,
            employee_id=employee_id)
        time_sheet = self.time_sheet_provider.update_with(time_sheet=time_sheet,
                                                          work_days_sheet=sheet,
                                                          norm=norm)
        time_sheet = self.calculator.calculate_vacation(time_sheet)
        self.storage.update(time_sheet)

    @classmethod
    def _calculate_norm_for_day(cls, time_sheet, day):
        current_date = datetime(time_sheet.year, time_sheet.month, 1)
        norm_calculator = TimeSheetInitHelper(current_date)
        norm = norm_calculator.calculate_norm_for_day(day)
        return norm


class CloseTimeSheetUseCase:
    def __init__(self, provider: TimeSheetProvider, storage: TimeSheetsStorage):
        self.provider = provider
        self.storage = storage

    def close_time_sheet(self, time_sheet_id):
        time_sheet = self.storage.find_by_id(time_sheet_id)
        time_sheet = self.provider.close(time_sheet)
        self.storage.update(time_sheet)


def _get_or_create(use_case, year, month, employee_id):
    time_sheet = use_case.storage.find_first_or_none(employee_id=employee_id,
                                                     year=year,
                                                     month=month)
    if not time_sheet:
        employee = use_case.employee_use_case.get_employee(employee_id)
        date = datetime(year, month, 1)
        time_sheet = use_case.time_sheet_provider.create_empty(
            employee_id=employee_id,
            date=date,
            rate=employee['rate'])
        use_case.storage.save(time_sheet)
    return time_sheet
