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

    def calculate_vacation(self, employee_id, sheet: dict,
                           date: datetime = datetime.now(), norm=None):
        employee = self.employee_storage.find_by_id(employee_id)
        time_sheet = self.time_sheet_provider.create(
            date=date, work_days_sheet=sheet, employee_id=employee.id,
            employee_rate=employee.rate)
        if not norm:
            time_sheet = self.calculator.calculate_norm(time_sheet)
        time_sheet = self.calculator.calculate_vacation(time_sheet)
        employee.vacation += time_sheet.vacation
        self.employee_storage.update(employee)
        self.time_sheet_storage.save(time_sheet)
