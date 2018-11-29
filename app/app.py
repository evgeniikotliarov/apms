from backend.domain.controllers.employee_provider import EmployeeProvider
from backend.utils.id_generator import IdGenerator


class App:
    def __init__(self):
        self.id_generator = IdGenerator()

    def create_employee(self, name, password, email):
        employee_id = self.id_generator.next_id()
        employee = EmployeeProvider.create_simple(employee_id, name, password, email)
        return employee
