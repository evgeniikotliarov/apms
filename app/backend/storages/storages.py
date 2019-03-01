from domain.models.employee import Employee
from domain.models.time_sheet import TimeSheet
from exceptions import EmailIsBusyError, NotFoundError, DbError
from storages.base_storage import Storage


class EmployeesStorage(Storage):
    def __init__(self, db):
        super().__init__(db, Employee)

    def find_by_email(self, email):
        found_employees = self.find_by(email=email)
        if not found_employees:
            raise NotFoundError("Employee with email {} not found".format(email))
        return found_employees[0]

    def save(self, entity):
        try:
            super().save(entity)
        except DbError:
            raise EmailIsBusyError

    def update(self, entity):
        try:
            super().update(entity)
        except DbError:
            raise EmailIsBusyError


class TimeSheetsStorage(Storage):
    def __init__(self, db):
        super().__init__(db, TimeSheet)
