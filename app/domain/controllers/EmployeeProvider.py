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
