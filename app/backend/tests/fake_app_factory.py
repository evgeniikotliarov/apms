from datetime import datetime

from app import App
from app_factory import IAppFactory, AppFactory
from domain.controllers.rate_calculator import RateCalculator
from tests import fixtures
from utils.hash_maker import ToHash


class TestAppFactory(IAppFactory):
    def create_app(self):
        return App()


class TestCopyOriginalAppFactory(AppFactory):
    def create_app(self):
        app = super().create_app()
        self.load_data(app)
        return app

    def load_data(self, app):
        serialized_employee = fixtures.load("admin_user")
        serialized_employee['password'] = ToHash().to_hash(serialized_employee['password'])
        admin_employee = self.employee_provider.deserialize(serialized_employee)
        serialized_employee = fixtures.load("unregistered_user")
        serialized_employee['password'] = ToHash().to_hash(serialized_employee['password'])
        unregistered_employee = self.employee_provider.deserialize(serialized_employee)
        self.employee_storage.save(admin_employee)
        self.employee_storage.save(unregistered_employee)
        app.create_time_sheet_use_case.create_time_sheet(
            date=datetime(2018, 1, 1),
            sheet=fixtures.load("january"),
            employee_id=1,
            rate=RateCalculator.MAX_DAYS,
            norm=23
        )
