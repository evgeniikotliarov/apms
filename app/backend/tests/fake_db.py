from datetime import datetime

from domain.controllers.employee_provider import EmployeeProvider
from domain.controllers.rate_calculator import RateCalculator
from domain.controllers.time_sheet_provider import TimeSheetProvider


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
            for param, value in kwargs.items():
                if getattr(entity, param) == value:
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
        self.january = {
            1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0,
            8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 0, 14: 0,
            15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 0, 21: 0,
            22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 0, 28: 0,
            29: 1, 30: 1, 31: 1
        }
        time_sheet = TimeSheetProvider.create(datetime.now(), self.january,
                                              0, RateCalculator.MIN_DAYS, norm=1)
        time_sheet.id = 0
        self.origin_entities.append(time_sheet)
        self.entities.append(time_sheet)
