import json

from controllers.controller_handler import authorized_controller_handler
from usecases.time_sheet_use_cases import GetTimeSheetUseCase, GetTimeSheetsUseCase, \
    UpdateTimeSheetUseCase
from utils.to_num_converter import ToNum


# noinspection PyUnusedLocal
class GetTimeSheetController:
    def __init__(self, use_case: GetTimeSheetUseCase):
        self.use_case = use_case
        self.user_email = None

    @authorized_controller_handler
    def on_get(self, request, response, time_sheet_id):
        converter = ToNum()
        time_sheet_id = converter.to_num(time_sheet_id)
        time_sheet = self.use_case.get_by_id(time_sheet_id)
        response.body = json.dumps(time_sheet)


# noinspection PyUnusedLocal
class EmployeeTimeSheetsController:
    def __init__(self,
                 get_use_case: GetTimeSheetsUseCase,
                 update_use_case: UpdateTimeSheetUseCase):
        self.get_use_case = get_use_case
        self.update_use_case = update_use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response, employee_id):
        year = request.media.get('year')
        month = request.media.get('month')
        converter = ToNum()
        year = converter.to_num(year)
        month = converter.to_num(month)
        employee_id = converter.to_num(employee_id)
        time_sheets = self.get_use_case.get_for_employee(employee_id, year, month)
        response.body = json.dumps(time_sheets)

    @authorized_controller_handler
    def on_patch(self, request, response, employee_id):
        year = request.media.get('year')
        month = request.media.get('month')
        sheet = request.media.get('sheet')
        converter = ToNum()
        year = converter.to_num(year)
        month = converter.to_num(month)
        employee_id = converter.to_num(employee_id)
        self.update_use_case.update_time_sheet_for(employee_id, year, month, sheet)


class GetEmployeesTimeSheetsController:
    def __init__(self, use_case: GetTimeSheetsUseCase):
        self.use_case = use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response):
        year = request.media.get('year')
        month = request.media.get('month')
        converter = ToNum()
        year = converter.to_num(year)
        month = converter.to_num(month)
        time_sheets = self.use_case.get_for_all_employees(year, month)
        response.body = json.dumps(time_sheets)
