import json

from controllers.controller_handler import authorized_controller_handler
from usecases.time_sheet_use_cases import GetTimeSheetUseCase, GetTimeSheetsUseCase


# noinspection PyUnusedLocal
class GetTimeSheetController:
    def __init__(self, use_cage: GetTimeSheetUseCase):
        self.use_cage = use_cage
        self.user_email = None

    @authorized_controller_handler
    def on_get(self, request, response, time_sheet_id):
        time_sheet = self.use_cage.get_by_id(int(time_sheet_id))
        response.body = json.dumps(time_sheet)


class GetEmployeeTimeSheetsController:
    def __init__(self, use_cage: GetTimeSheetsUseCase):
        self.use_cage = use_cage
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response, employee_id):
        year = request.media.get('year')
        year = int(year) if year else None
        month = request.media.get('month')
        month = int(month) if month else None
        time_sheets = self.use_cage.get_for_employee(int(employee_id), year, month)
        response.body = json.dumps(time_sheets)


class GetEmployeesTimeSheetsController:
    def __init__(self, use_cage: GetTimeSheetsUseCase):
        self.use_cage = use_cage
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response):
        year = request.media.get('year')
        year = int(year) if year else None
        month = request.media.get('month')
        month = int(month) if month else None
        time_sheets = self.use_cage.get_for_all_employees(year, month)
        response.body = json.dumps(time_sheets)
