from datetime import datetime

from app import App
from app_factory import IAppFactory, AppFactory
from domain.controllers.rate_calculator import RateCalculator
from tests.fixtures.sheets import january


class TestAppFactory(IAppFactory):
    def create_app(self):
        return App()


class TestCopyOriginalAppFactory(AppFactory):
    def create_app(self):
        app = super().create_app()
        self.load_data(app)
        return app

    @classmethod
    def load_data(cls, app):
        app.create_employee_use_case.create_employee(
            'name',
            'password',
            'some@mail.com')
        app.create_time_sheet_use_case.create_time_sheet(
            date=datetime(2018, 1, 1),
            sheet=january,
            employee_id=1,
            rate=RateCalculator.MAX_DAYS,
            norm=23
        )
