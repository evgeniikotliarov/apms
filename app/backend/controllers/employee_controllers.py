import json
from datetime import datetime

import falcon

from controllers.controller_handler import controller_handler, authorized_controller_handler
from usecases.employee_use_cases import CreateEmployeeUseCase, GetEmployeeUseCase, \
    GetAllEmployeeUseCase, CheckEmployeeUseCase, RegisterEmployeeUseCase, CheckAdminRightsUseCase


class RegistrationEmployeeController:
    def __init__(self, use_cage: CreateEmployeeUseCase):
        self.use_cage = use_cage

    @controller_handler
    def on_post(self, request, response):
        name = request.media['name']
        password = request.media['password']
        email = request.media['email']
        token = self.use_cage.create_employee(name=name, password=password, email=email)
        response.body = json.dumps({'token': token})
        response.status = falcon.HTTP_201


class AuthenticationEmployeeController:
    def __init__(self, use_cage: CheckEmployeeUseCase):
        self.use_cage = use_cage

    @controller_handler
    def on_post(self, request, response):
        email = request.media['email']
        password = request.media['password']
        token = self.use_cage.check_employee(password=password, email=email)
        response.body = json.dumps({'token': token})


class AcceptEmployeeController:
    def __init__(self,
                 check_admin_use_case: CheckAdminRightsUseCase,
                 accept_use_cage: RegisterEmployeeUseCase):
        self.accept_use_cage = accept_use_cage
        self.check_admin_use_case = check_admin_use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response, employee_id):
        self.check_admin_use_case.check_rights(self.user_email)

        date = datetime.strptime(request.media['employment_date'], '%Y.%m.%d')
        vacation = float(request.media['vacation'])

        self.accept_use_cage.register_employee(employee_id, date, vacation)
        response.status = falcon.HTTP_201


# noinspection PyUnusedLocal
class GetEmployeeController:
    def __init__(self, use_cage: GetEmployeeUseCase):
        self.use_cage = use_cage
        self.user_email = None

    @authorized_controller_handler
    def on_get(self, request, response, employee_id):
        employee = self.use_cage.get_employee(int(employee_id))
        response.body = json.dumps(employee)


# noinspection PyUnusedLocal
class GetEmployeesController:
    def __init__(self, use_cage: GetAllEmployeeUseCase):
        self.use_cage = use_cage
        self.user_email = None

    @authorized_controller_handler
    def on_get(self, request, response):
        employees = self.use_cage.get_employees()
        response.body = json.dumps(employees)
