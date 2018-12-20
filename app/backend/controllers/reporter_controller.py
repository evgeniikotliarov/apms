from datetime import datetime

import falcon
import msgpack

from controllers.controller_handler import authorized_controller_handler
# noinspection PyUnusedLocal
from usecases.reporter_use_case import ReporterUseCase
from utils.to_num_converter import ToNum


class ReporterController:
    def __init__(self, use_case: ReporterUseCase):
        self.use_case = use_case
        self.user_email = None

    @authorized_controller_handler
    def on_post(self, request, response):
        # TODO: добавил для примера, необходимо дописать тесты и проверить на скачивание файла
        # TODO, возможно изменить способ прикрепления файла к response
        # TODO: http://falcon.readthedocs.io/en/stable/user/tutorial.html#creating-resources
        year = request.media['year']
        month = request.media['month']
        converter = ToNum()
        year = converter.to_num(year)
        month = converter.to_num(month)
        report_path = self.use_case.get_formed_report_by_date(date=datetime(year, month, 1))
        report = {
            'report': report_path
        }
        response.data = msgpack.packb(report, use_bin_type=True)
        report.content_type = falcon.MEDIA_MSGPACK
