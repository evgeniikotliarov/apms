from domain.models.employee import Employee
from domain.models.time_sheet import TimeSheet
from storages.employees_storage import Storage


class EmployeesStorage(Storage):
    def __init__(self, db):
        super().__init__(db, Employee)


class TimeSheetsStorage(Storage):
    def __init__(self, db):
        super().__init__(db, TimeSheet)
