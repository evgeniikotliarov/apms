from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage


class CalculateVacationUseCase:
    def __init__(self,
                 calculator: VacationCalculator,
                 employee_storage: EmployeesStorage,
                 time_sheet_storage: TimeSheetsStorage):
        self.calculator = calculator
        self.employee_storage = employee_storage
        self.time_sheet_storage = time_sheet_storage

    def calculate_vacation(self, time_sheet_id):
        time_sheet = self.time_sheet_storage.find_by_id(time_sheet_id)
        employee = self.employee_storage.find_by_id(time_sheet.employee_id)
        time_sheet.rate = employee.rate
        if time_sheet.vacation:
            employee.vacation -= time_sheet.vacation
        time_sheet = self._calculate_vac(time_sheet)
        self._update_employee_vacation(employee, time_sheet)

    def _calculate_vac(self, time_sheet):
        if not time_sheet.norm:
            time_sheet = self.calculator.calculate_norm(time_sheet)
        time_sheet = self.calculator.calculate_vacation(time_sheet)
        return time_sheet

    def _update_employee_vacation(self, employee, time_sheet):
        employee.vacation += time_sheet.vacation
        self.employee_storage.update(employee)
        self.time_sheet_storage.update(time_sheet)
