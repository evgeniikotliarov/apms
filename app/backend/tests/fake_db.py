from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.db.db_builder import DbBuilder
from tests import fixtures


class FakeDb(DbBuilder):
    def build(self):
        session = super().build()
        admin = EmployeeProvider.deserialize(fixtures.load("admin_user"))
        unaccepted_user = EmployeeProvider.deserialize(fixtures.load("unaccepted_user"))
        user_with_vacation = EmployeeProvider.deserialize(fixtures.load("user_with_vacation"))
        session.add(admin)
        session.add(unaccepted_user)
        session.add(user_with_vacation)
        session.commit()
        time_sheet = TimeSheetProvider.create(datetime(2010, 1, 1), fixtures.load("january"),
                                              0, RateCalculator.MIN_DAYS, norm=1)
        time_sheet.id = 0
        time_sheet.vacation = 10
        session.add(time_sheet)
        session.commit()
        return session
