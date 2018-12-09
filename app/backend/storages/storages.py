from domain.models.employee import Employee
from domain.models.time_sheet import TimeSheet
from exceptions import EmailBusyException
from storages.base_storage import Storage


class EmployeesStorage(Storage):
    def __init__(self, db):
        super().__init__(db, Employee)

    def find_by_email(self, email):
        return self.find_by(email=email)[0]

    def save(self, entity):
        exist_employee = self.find_by(email=entity.email)
        if exist_employee:
            raise EmailBusyException
        else:
            super().save(entity)

    def update(self, entity):
        exist_employee = self.find_by(email=entity.email)
        if exist_employee.__len__() > 1:
            raise EmailBusyException
        else:
            super().update(entity)


class TimeSheetsStorage(Storage):
    def __init__(self, db):
        super().__init__(db, TimeSheet)
