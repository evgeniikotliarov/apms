from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from exceptions import AuthenticationError, NotFoundError, AuthorizationError, \
    DeactivatedEmployeeError, UpdatingError
from storages.storages import EmployeesStorage
from utils.hash_maker import ToHash
from utils.tokenizer import Tokenizer


class GetEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def get_employee(self, employee_id):
        employee = self.storage.find_by_id(employee_id)
        return self.employee_provider.serialize(employee)

    def get_employee_by_email(self, email):
        employee = self.storage.find_by_email(email)
        return self.employee_provider.serialize(employee)


class GetAllEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def get_employees(self):
        employees = self.storage.get_all()
        serialized_employees = []
        for employee in employees:
            serialized_employee = self.employee_provider.serialize(employee)
            serialized_employees.append(serialized_employee)
        return serialized_employees


class CreateEmployeeUseCase:
    def __init__(self,
                 employee_provider: EmployeeProvider,
                 storage: EmployeesStorage,
                 tokenizer: Tokenizer,
                 hash_maker: ToHash):
        self.employee_provider = employee_provider
        self.hash_maker = hash_maker
        self.tokenizer = tokenizer
        self.storage = storage

    def create_employee(self, name, password, email):
        password = self.hash_maker.to_hash(password)
        employee = self.employee_provider.create_simple(name, password, email)
        self.storage.save(employee)
        token_data = {'email': email, 'password': password}
        return self.tokenizer.get_token_by_data(token_data)


class CheckEmployeeUseCase:
    def __init__(self,
                 employee_provider: EmployeeProvider,
                 storage: EmployeesStorage,
                 tokenizer: Tokenizer,
                 hash_maker: ToHash):
        self.employee_provider = employee_provider
        self.hash_maker = hash_maker
        self.tokenizer = tokenizer
        self.storage = storage

    def check_employee(self, email, password):
        try:
            employee = self.storage.find_by_email(email)
            check_password = self.hash_maker.check_with_hash(password, employee.password)
            if not check_password:
                raise AuthenticationError()
            if not employee.activated:
                raise DeactivatedEmployeeError()
            token_data = {'email': email, 'password': employee.password}
            return self.tokenizer.get_token_by_data(token_data)
        except NotFoundError:
            raise AuthenticationError()


class CheckAdminRightsUseCase:
    def __init__(self, storage: EmployeesStorage):
        self.storage = storage

    def check_rights(self, email):
        employee = self.storage.find_by_email(email)
        if not employee.is_admin:
            raise AuthorizationError()


class RegisterEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def register_employee(self, employee_id, employment_date: datetime, balance_vac=0):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.register(employee, employment_date, balance_vac)
        self.storage.update(employee)


class UpdateEmployeeUseCase:
    def __init__(self, to_hash: ToHash,
                 employee_provider: EmployeeProvider,
                 storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage
        self.to_hash = to_hash

    def update_employee(self, employee_id,
                        name=None,
                        old_password=None,
                        new_password=None,
                        email=None):
        employee = self.storage.find_by_id(employee_id)
        password = None
        if old_password:
            if self.to_hash.check_with_hash(old_password, employee.password) and new_password:
                password = self.to_hash.to_hash(new_password)
            else:
                raise UpdatingError()
        employee = self.employee_provider.update_with(employee=employee,
                                                      name=name,
                                                      password=password,
                                                      email=email)
        self.storage.update(employee)


class AdminRightsEmployeeUseCase:
    def __init__(self, employee_provider: EmployeeProvider, storage: EmployeesStorage):
        self.employee_provider = employee_provider
        self.storage = storage

    def grant_to_admin(self, employee_id):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.grant_to_admin(employee)
        self.storage.update(employee)

    def pick_up_admin(self, employee_id):
        employee = self.storage.find_by_id(employee_id)
        employee = self.employee_provider.pick_up_admin(employee)
        self.storage.update(employee)
