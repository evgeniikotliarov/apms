from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage


class CalculateVacationUseCase:
    def __init__(self, employee_provider: EmployeeProvider,
                 time_sheet_provider: TimeSheetProvider,
                 calculator: VacationCalculator,
                 employee_storage: EmployeesStorage,
                 time_sheet_storage: TimeSheetsStorage):
        self.employee_provider = employee_provider
        self.time_sheet_provider = time_sheet_provider
        self.calculator = calculator
        self.employee_storage = employee_storage
        self.time_sheet_storage = time_sheet_storage

    def calculate_vacation(self, employee_id, sheet,
                           date: datetime = datetime.now(), norm=None):
        time_sheets = self.time_sheet_storage.find_by(year=date.year, month=date.month,
                                                      employee_id=employee_id)
        if time_sheets and time_sheets.first():
            self._recalculate(employee_id, time_sheets.first(), norm, sheet)
        else:
            self._calculate_as_new(date, employee_id, norm, sheet)

    def _calculate_as_new(self, date, employee_id, norm, sheet):
        employee = self.employee_storage.find_by_id(employee_id)
        time_sheet = self.time_sheet_provider.create(
            date=date, work_days_sheet=sheet, employee_id=employee.id,
            employee_rate=employee.rate)
        time_sheet = self.__calculate_vac(norm, time_sheet)
        self.__update_employee_vacation(employee, time_sheet)

    def _recalculate(self, employee_id, time_sheet, norm, sheet):
        employee = self.employee_storage.find_by_id(employee_id)
        employee.vacation -= time_sheet.vacation
        time_sheet.sheet = sheet
        time_sheet = self.__calculate_vac(norm, time_sheet)
        self.__update_employee_vacation(employee, time_sheet)

    def __calculate_vac(self, norm, time_sheet):
        if not norm:
            time_sheet = self.calculator.calculate_norm(time_sheet)
        time_sheet = self.calculator.calculate_vacation(time_sheet)
        return time_sheet

    def __update_employee_vacation(self, employee, time_sheet):
        employee.vacation += time_sheet.vacation
        self.employee_storage.update(employee)
        self.time_sheet_storage.update(time_sheet)
