from app import App
from controllers.employee_controllers import CreateEmployeeController, GetEmployeeController, \
    GetEmployeesController
from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.db.db_builder import DbBuilder
from storages.storages import TimeSheetsStorage, EmployeesStorage
from usecases.employee_use_cases import CreateEmployeeUseCase, GetEmployeeUseCase, \
    GetAllEmployeeUseCase, RegisterEmployeeUseCase, UpdateEmployeeUseCase, \
    AdminRightsEmployeeUseCase
from usecases.time_sheet_use_cases import GetTimeSheetUseCase, GetAllTimeSheetUseCase, \
    CreateTimeSheetUseCase, UpdateTimeSheetUseCase, CloseTimeSheetUseCase


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

        employee_storage = EmployeesStorage(self.db)
        employee_provider = EmployeeProvider()

        self.app.get_employee_use_case = GetEmployeeUseCase(employee_provider,
                                                            employee_storage)
        self.app.get_employees_use_case = GetAllEmployeeUseCase(employee_provider,
                                                                employee_storage)
        self.app.create_employee_use_case = CreateEmployeeUseCase(employee_provider,
                                                                  employee_storage)
        self.app.register_employee_use_case = RegisterEmployeeUseCase(employee_provider,
                                                                      employee_storage)
        self.app.update_employee_use_case = UpdateEmployeeUseCase(employee_provider,
                                                                  employee_storage)
        self.app.admin_rights_employee_use_case = AdminRightsEmployeeUseCase(employee_provider,
                                                                             employee_storage)

        time_sheet_storage = TimeSheetsStorage(self.db)
        time_sheet_provider = TimeSheetProvider()

        self.app.get_time_sheet_use_case = GetTimeSheetUseCase(time_sheet_provider,
                                                               time_sheet_storage)
        self.app.get_time_sheets_use_case = GetAllTimeSheetUseCase(time_sheet_provider,
                                                                   time_sheet_storage)
        self.app.create_time_sheet_use_case = CreateTimeSheetUseCase(time_sheet_provider,
                                                                     time_sheet_storage)
        self.app.update_time_sheet_use_case = UpdateTimeSheetUseCase(time_sheet_provider,
                                                                     time_sheet_storage)
        self.app.close_time_sheet_use_case = CloseTimeSheetUseCase(time_sheet_provider,
                                                                   time_sheet_storage)

        self.create_employee_controller = CreateEmployeeController(
            self.app.create_employee_use_case)
        self.get_employee_controller = GetEmployeeController(self.app.get_employee_use_case)
        self.get_employees_controller = GetEmployeesController(self.app.get_employees_use_case)
        self._init_routes()
        return self.app

    def _init_routes(self):
        self.app.add_route('/api/employees/create', self.create_employee_controller)
        self.app.add_route('/api/employees/{employee_id}', self.get_employee_controller)
        self.app.add_route('/api/employees', self.get_employees_controller)
