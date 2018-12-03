from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.storages import EmployeesStorage


class CalculateVacationUseCase:
    def __init__(self, employee_provider: EmployeeProvider, time_sheet_provider: TimeSheetProvider,
                 time_sheet_storage: TimeSheetStorage, employee_storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.time_sheet_provider = time_sheet_provider
        self.employee_storage = employee_storage
        self.time_sheet_storage = time_sheet_storage

    def calculate_vacation(self, employee_id):
        employee = self.employee_storage.find_by_id(employee_id)
        time_sheet = self.time_sheet_provider
        self.storage.update(employee)
        return employee
