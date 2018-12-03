from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from storages.storages import EmployeesStorage


class CreateEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def create_employee(self, name, password, email):
        employee = self.employee_provider.create_simple(name, password, email)
        self.storage.save(employee)
        return employee


class RegisterEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def register_employee(self, employee_id, employment_date: datetime, balance_vac=0):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.register(employee, employment_date, balance_vac)
        self.storage.update(employee)
        return employee


class UpdateEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def update_employee(self, employee_id, name=None, password=None, email=None):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.update_with(employee, name, password, email)
        self.storage.update(employee)
        return employee


class AdminRightsEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def grant_to_admin(self, employee_id):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.grant_to_admin(employee)
        self.storage.update(employee)
        return employee

    def pick_up_admin(self, employee_id):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.pick_up_admin(employee)
        self.storage.update(employee)
        return employee