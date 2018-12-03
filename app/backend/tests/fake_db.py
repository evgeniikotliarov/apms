from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider
# noinspection PyPackageRequirements
from tests.fixtures.sheets import january


class List(list):
    def first(self):
        return self[0]

    def all(self):
        return List(self)


class Query:
    def __init__(self, entities):
        self.entities = entities

    def filter_by(self, **kwargs):
        if kwargs == {}:
            return self.entities
        found_entities = List()
        for entity in self.entities:
            check_condition = True
            for param, value in kwargs.items():
                check_condition = check_condition and getattr(entity, param) == value
            if check_condition:
                found_entities.append(entity)
        return found_entities


class FakeBaseDb:
    def __init__(self):
        self.entities = List()
        self.origin_entities = List()

    def add(self, entity):
        for ent in self.entities:
            if ent.id == entity.id:
                self.entities.remove(ent)
        if not entity.id:
            entity.id = self.entities.__len__()
        self.entities.append(entity)

    def query(self, _):
        query = Query(self.origin_entities)
        return query

    def all(self):
        return self.entities

    def save(self, employee):
        self.entities.append(employee.__dict__)

    def commit(self):
        self.origin_entities = self.entities

    def rollback(self):
        self.entities = self.origin_entities


class FakeEmployeesDb(FakeBaseDb):
    def __init__(self):
        super().__init__()
        employee = EmployeeProvider.create_simple('name', 'password', 'some@mail.com')
        employee.id = 0
        self.origin_entities.append(employee)
        self.entities.append(employee)


class FakeTimeSheetsDb(FakeBaseDb):
    def __init__(self):
        super().__init__()
        time_sheet = TimeSheetProvider.create(datetime(2010, 1, 1), january,
                                              0, RateCalculator.MIN_DAYS, norm=1)
        time_sheet.id = 0
        time_sheet.vacation = 10
        self.origin_entities.append(time_sheet)
        self.entities.append(time_sheet)
