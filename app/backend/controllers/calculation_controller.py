import json

from controllers.controller_handler import authorized_controller_handler
from usecases.calculate_vacation_use_case import CalculateVacationUseCase


# noinspection PyUnusedLocal
class VacationCalculatorController:
    def __init__(self, use_case: CalculateVacationUseCase):
        self.use_case = use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response, employee_id):
        year = request.media['year']
        month = request.media['month']
        norm = request.media.get('norm')
        employee = self.use_case.calculate_vacation_for(int(employee_id), year, month, norm)
        response.body = json.dumps(employee)
