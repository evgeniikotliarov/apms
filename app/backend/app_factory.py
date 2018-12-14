from app import App
from controllers.calculation_controller import VacationCalculatorController
from controllers.employee_controllers import RegistrationEmployeeController, \
    GetEmployeeController, GetEmployeesController, AuthenticationEmployeeController, \
    AcceptEmployeeController
from controllers.time_sheet_controllers import GetTimeSheetController, \
    EmployeeTimeSheetsController, GetEmployeesTimeSheetsController
from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from domain.controllers.vacation_calculator import VacationCalculator
from storages.db.db_builder import DbBuilder
from storages.storages import TimeSheetsStorage, EmployeesStorage
from usecases.calculate_vacation_use_case import CalculateVacationUseCase
from usecases.employee_use_cases import CreateEmployeeUseCase, GetEmployeeUseCase, \
    GetAllEmployeeUseCase, RegisterEmployeeUseCase, UpdateEmployeeUseCase, \
    AdminRightsEmployeeUseCase, CheckEmployeeUseCase, CheckAdminRightsUseCase
from usecases.time_sheet_use_cases import GetTimeSheetUseCase, GetTimeSheetsUseCase, \
    CreateTimeSheetUseCase, UpdateTimeSheetUseCase, CloseTimeSheetUseCase
from utils.hash_maker import ToHash
from utils.tokenizer import Tokenizer


class IAppFactory:
    def create_app(self) -> App:
        raise NotImplementedError()


# noinspection PyAttributeOutsideInit
class AppFactory(IAppFactory):
    def __init__(self):
        self.db = None
        self.app = None

    def create_app(self):
        if self.app is None:
            self.app = App()

        if self.db is None:
            self.db = DbBuilder().build()

        self.employee_storage = EmployeesStorage(self.db)
        self.employee_provider = EmployeeProvider()

        self.tokenizer = Tokenizer()
        self.to_hash = ToHash()

        self.app.get_employee_use_case = GetEmployeeUseCase(self.employee_provider,
                                                            self.employee_storage)
        self.app.get_employees_use_case = GetAllEmployeeUseCase(self.employee_provider,
                                                                self.employee_storage)
        self.app.create_employee_use_case = CreateEmployeeUseCase(self.employee_provider,
                                                                  self.employee_storage,
                                                                  self.tokenizer,
                                                                  self.to_hash)
        self.app.check_employee_use_case = CheckEmployeeUseCase(self.employee_provider,
                                                                self.employee_storage,
                                                                self.tokenizer,
                                                                self.to_hash)
        self.app.check_admin_rights_use_case = CheckAdminRightsUseCase(self.employee_storage)
        self.app.register_employee_use_case = RegisterEmployeeUseCase(self.employee_provider,
                                                                      self.employee_storage)
        self.app.update_employee_use_case = UpdateEmployeeUseCase(self.employee_provider,
                                                                  self.employee_storage)
        self.app.admin_rights_employee_use_case = AdminRightsEmployeeUseCase(self.employee_provider,
                                                                             self.employee_storage)

        self.time_sheet_storage = TimeSheetsStorage(self.db)
        self.time_sheet_provider = TimeSheetProvider()

        self.app.get_time_sheet_use_case = GetTimeSheetUseCase(self.time_sheet_provider,
                                                               self.time_sheet_storage)
        self.app.get_time_sheets_use_case = GetTimeSheetsUseCase(self.time_sheet_provider,
                                                                 self.time_sheet_storage)
        self.app.create_time_sheet_use_case = CreateTimeSheetUseCase(self.time_sheet_provider,
                                                                     self.time_sheet_storage)
        self.app.update_time_sheet_use_case = UpdateTimeSheetUseCase(self.time_sheet_provider,
                                                                     self.time_sheet_storage)
        self.app.close_time_sheet_use_case = CloseTimeSheetUseCase(self.time_sheet_provider,
                                                                   self.time_sheet_storage)

        self.vacation_calculator = VacationCalculator()

        self.app.calculate_vacation_use_case = CalculateVacationUseCase(self.vacation_calculator,
                                                                        self.employee_storage,
                                                                        self.time_sheet_storage)

        self.registration_employee_controller = RegistrationEmployeeController(
            self.app.create_employee_use_case)
        self.authentication_employee_controller = AuthenticationEmployeeController(
            self.app.check_employee_use_case)
        self.accept_employee_controller = AcceptEmployeeController(
            self.app.check_admin_rights_use_case,
            self.app.register_employee_use_case)
        self.get_employee_controller = GetEmployeeController(self.app.get_employee_use_case)
        self.get_employees_controller = GetEmployeesController(self.app.get_employees_use_case)

        self.get_time_sheet_controller = GetTimeSheetController(self.app.get_time_sheet_use_case)
        self.employee_time_sheets_controller = EmployeeTimeSheetsController(
            self.app.get_time_sheets_use_case, self.app.update_time_sheet_use_case)
        self.get_employees_time_sheets_controller = GetEmployeesTimeSheetsController(
            self.app.get_time_sheets_use_case)

        self.calculate_vacation_controller = VacationCalculatorController(
            self.app.calculate_vacation_use_case)

        self._init_routes()
        return self.app

    def _init_routes(self):
        self.app.add_route('/api/sign-up', self.registration_employee_controller)
        self.app.add_route('/api/logдв-in', self.authentication_employee_controller)
        self.app.add_route('/api/employees/{employee_id}/register', self.accept_employee_controller)
        self.app.add_route('/api/employees/{employee_id}', self.get_employee_controller)
        self.app.add_route('/api/employees', self.get_employees_controller)

        self.app.add_route('/api/time-sheets/{time_sheets_id}', self.get_time_sheet_controller)
        self.app.add_route('/api/employees/{employee_id}/time-sheets',
                           self.employee_time_sheets_controller)
        self.app.add_route('/api/employees/time-sheets', self.get_employees_time_sheets_controller)

        self.app.add_route('/api/employees/{employee_id}/vacation',
                           self.calculate_vacation_controller)
