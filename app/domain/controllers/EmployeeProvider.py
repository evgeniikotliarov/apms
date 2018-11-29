from datetime import datetime

from domain.models.Employee import Employee


class EmployeeProvider:
    @staticmethod
    def create_simple(employee_id, name, password, email):
        employee = Employee()
        employee.name = name
        employee.password = password
        employee.email = email
        employee.id = employee_id
        return employee

    @staticmethod
    def register_user(employee, employment_date, balance_vac=0):
        employee.registration_date = datetime.now()
        employee.employment_date = employment_date
        employee.vacation = balance_vac
        return employee
