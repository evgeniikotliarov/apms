from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage


class CalculateVacationUseCase:
    def __init__(self,
                 vac_calculator: VacationCalculator,
                 employee_storage: EmployeesStorage,
                 time_sheet_storage: TimeSheetsStorage):
        self.vac_calculator = vac_calculator
        self.employee_storage = employee_storage
        self.time_sheet_storage = time_sheet_storage

    def calculate_vacation(self, time_sheet_id, norm=None):
        time_sheet = self.time_sheet_storage.find_by_id(time_sheet_id)
        return self._calculate_by_time_sheet(norm, time_sheet)

    def calculate_vacation_for(self, employee_id, year, month, norm=None):
        time_sheet = self.time_sheet_storage.find_first_by(
            employee_id=employee_id,
            year=year,
            month=month)
        return self._calculate_by_time_sheet(norm, time_sheet)

    def _calculate_by_time_sheet(self, norm, time_sheet):
        employee = self.employee_storage.find_by_id(time_sheet.employee_id)
        time_sheet.rate = employee.rate
        if norm:
            time_sheet.norm = norm
        if time_sheet.vacation:
            employee.vacation -= time_sheet.vacation
        time_sheet = self._calculate_vac(time_sheet)
        self._update_employee_vacation(employee, time_sheet)
        return {'month_vacation': time_sheet.vacation, 'total_vacation': employee.vacation}

    def _calculate_vac(self, time_sheet):
        time_sheet = self.vac_calculator.calculate_vacation(time_sheet)
        return time_sheet

    def _update_employee_vacation(self, employee, time_sheet):
        employee.vacation += time_sheet.vacation
        self.employee_storage.update(employee)
        self.time_sheet_storage.update(time_sheet)
