import json

from controllers.controller_handler import authorized_controller_handler
from usecases.calculate_vacation_use_case import CalculateVacationUseCase
from utils.to_num_converter import ToNum


class VacationCalculatorController:
    def __init__(self, use_case: CalculateVacationUseCase):
        self.use_case = use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response, employee_id):
        year = request.media.get('year')
        month = request.media.get('month')
        norm = request.media.get('norm')
        converter = ToNum()
        year = converter.to_num(year)
        month = converter.to_num(month)
        norm = converter.to_num(norm)
        employee_id = converter.to_num(employee_id)

        employee = self.use_case.calculate_vacation_for(employee_id, year, month, norm)
        response.body = json.dumps(employee)
