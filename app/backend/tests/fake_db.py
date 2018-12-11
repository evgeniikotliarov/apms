from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.time_sheet_provider import TimeSheetProvider
from storages.db.db_builder import DbBuilder
from tests import fixtures


class FakeDb(DbBuilder):
    def build(self):
        session = super().build()
        admin_user = EmployeeProvider.deserialize(fixtures.load("admin_user"))
        unaccepted_user = EmployeeProvider.deserialize(fixtures.load("unaccepted_user"))
        user_with_vacation = EmployeeProvider.deserialize(fixtures.load("user_with_vacation"))
        session.add(admin_user)
        session.add(unaccepted_user)
        session.add(user_with_vacation)
        session.commit()

        january_ts = TimeSheetProvider.deserialize(fixtures.load('january_time_sheet'))
        half_january_ts = TimeSheetProvider.deserialize(fixtures.load('half_january_time_sheet'))
        session.add(january_ts)
        session.add(half_january_ts)
        session.commit()
        return session
