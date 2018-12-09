from datetime import datetime

from domain.models.employee import Employee


class EmployeeProvider:
    @classmethod
    def create_simple(cls, name, password, email):
        employee = Employee()
        employee.name = name
        employee.email = email
        employee.password = password
        employee.activated = False
        employee.is_admin = False
        return employee

    @classmethod
    def register(cls, employee: Employee, employment_date: datetime, balance_vac=0):
        employee.registration_date = datetime.now()
        employee.employment_date = employment_date
        employee.activated = True
        employee.vacation = balance_vac
        return employee

    @classmethod
    def update_with(cls, employee: Employee, name=None, password=None, email=None,
                    employment_date: datetime = None):
        employee.employment_date = employment_date if employment_date else employee.employment_date
        employee.password = password if password else employee.password
        employee.email = email if email else employee.email
        employee.name = name if name else employee.name
        return employee

    @classmethod
    def activate(cls, employee: Employee):
        employee.activated = True
        return employee

    @classmethod
    def deactivate(cls, employee: Employee):
        employee.activated = False
        return employee

    @classmethod
    def set_balance_vac(cls, employee: Employee, balance_vac):
        employee.vacation = balance_vac
        return employee

    @classmethod
    def grant_to_admin(cls, employee: Employee):
        employee.is_admin = True
        return employee

    @classmethod
    def pick_up_admin(cls, employee: Employee):
        employee.is_admin = False
        return employee

    @classmethod
    def serialize(cls, employee: Employee):
        serialized_employee = {
            'id': employee.id,
            'name': employee.name,
            'password': employee.password,
            'email': employee.email,
            'vacation': employee.vacation,
            'is_admin': employee.is_admin,
            'activated': employee.activated,
            'employment_date': None,
            'registration_date': None
        }
        if employee.employment_date:
            serialized_employee['employment_date'] = employee.employment_date \
                .strftime('%Y.%m.%d')
        if employee.registration_date:
            serialized_employee['registration_date'] = employee.registration_date \
                .strftime('%Y.%m.%d')
        return serialized_employee

    @classmethod
    def deserialize(cls, serialized_employee: dict):
        employee = Employee()
        for key, value in serialized_employee.items():
            if 'date' in key and value:
                value = datetime.strptime(value, '%Y.%m.%d')
            setattr(employee, key, value)
        return employee
