from datetime import datetime

from backend.domain.models.Employee import Employee


class EmployeeProvider:
    @staticmethod
    def create_simple(employee_id, name, password, email):
        employee = Employee()
        employee.id = employee_id
        employee.name = name
        employee.password = password
        employee.email = email
        employee.activated = False
        return employee

    @staticmethod
    def register(employee, employment_date, balance_vac=0):
        employee.registration_date = datetime.now()
        employee.employment_date = employment_date
        employee.vacation = balance_vac
        employee.activated = True
        return employee

    @staticmethod
    def update_with(employee, name=None, password=None, email=None, employment_date=None):
        employee.employment_date = employment_date if employment_date else employee.employment_date
        employee.password = password if password else employee.password
        employee.email = email if email else employee.email
        employee.name = name if name else employee.name
        return employee