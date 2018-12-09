from app import App
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

        self.get_employee_use_case = GetEmployeeUseCase(employee_provider,
                                                        employee_storage)
        self.get_employees_use_case = GetAllEmployeeUseCase(employee_provider,
                                                            employee_storage)
        self.create_employee_use_case = CreateEmployeeUseCase(employee_provider,
                                                              employee_storage)
        self.register_employee_use_case = RegisterEmployeeUseCase(employee_provider,
                                                                  employee_storage)
        self.update_employee_use_case = UpdateEmployeeUseCase(employee_provider,
                                                              employee_storage)
        self.admin_rights_employee_use_case = AdminRightsEmployeeUseCase(employee_provider,
                                                                         employee_storage)

        time_sheet_storage = TimeSheetsStorage(self.db)
        time_sheet_provider = TimeSheetProvider()

        self.get_time_sheet_use_case = GetTimeSheetUseCase(time_sheet_provider,
                                                           time_sheet_storage)
        self.get_time_sheets_use_case = GetAllTimeSheetUseCase(time_sheet_provider,
                                                               time_sheet_storage)
        self.create_time_sheet_use_case = CreateTimeSheetUseCase(time_sheet_provider,
                                                                 time_sheet_storage)
        self.update_time_sheet_use_case = UpdateTimeSheetUseCase(time_sheet_provider,
                                                                 time_sheet_storage)
        self.close_time_sheet_use_case = CloseTimeSheetUseCase(time_sheet_provider,
                                                               time_sheet_storage)