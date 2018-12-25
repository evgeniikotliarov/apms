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
    def __init__(self):
        super().__init__()
        self.tokens = {}

    def create_app(self):
        self.app = super().create_app()
        self.load_data()
        return self.app

    def load_data(self):
        self.__load_user('admin_user')
        self.__load_user('unaccepted_user')
        self.__load_user('unactivated_user')
        self.__load_user('user_with_vacation')
        self.__create_and_load_time_sheet(date=datetime(2018, 2, 1))
        self.__create_and_load_time_sheet(employee_id=3)

    def __create_and_load_time_sheet(self,
                                     date: datetime = datetime(2018, 1, 1),
                                     sheet=fixtures.load('february'),
                                     employee_id=0,
                                     rate=RateCalculator.MIN_DAYS,
                                     norm=21):
        self.app.create_time_sheet_use_case.create_time_sheet(
            date=date, sheet=sheet, employee_id=employee_id, rate=rate, norm=norm
        )

    def __load_user(self, name):
        serialized_employee = fixtures.load(name)
        password = ToHash().to_hash(serialized_employee['password'])
        serialized_employee['password'] = password
        employee = self.employee_provider.deserialize(serialized_employee)
        self.employee_storage.save(employee)
        email = serialized_employee['email']
        data = {'email': email, 'password': password}
        self.tokens[email] = self.tokenizer.get_token_by_data(data)
