from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float, Boolean, \
    create_engine, DateTime, Text
from sqlalchemy.orm import sessionmaker, mapper, relationship, clear_mappers

import settings
from domain.models.employee import Employee
from domain.models.time_sheet import TimeSheet
from storages.db.suctom_type import ArrayType


class DbBuilder:
    def __init__(self):
        self.session = None
        self.engine = None
        self.metadata = None
        self.employees = None
        self.time_sheets = None

    def build(self):
        self.create_engine()
        self.create_schema()
        self.create_session()
        return self.session

    def create_session(self):
        if self.session is None:
            session = sessionmaker(self.engine)
            self.session = session()
        return self.session

    def create_engine(self):
        if self.engine is None:
            self.engine = create_engine(settings.DB_CONNECTION_STRING)
            self.metadata = MetaData(bind=self.engine)
        return self.engine

    def create_schema(self):
        self.__build_employee_schema()
        self.__build_time_sheet_schema()
        self.__map_entities()
        self.metadata.create_all(self.engine)

    def __build_employee_schema(self):
        self.employees = Table(
            'employees', self.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('name', String(32), index=True, nullable=False),
            Column('password', String(32), nullable=False),
            Column('email', String(64), unique=True, nullable=False),
            Column('vacation', Float(8), nullable=True),
            Column('activated', Boolean, nullable=False),
            Column('is_admin', Boolean, nullable=False),
            Column('employment_date', DateTime, nullable=True),
            Column('acceptance_date', DateTime, nullable=True)
        )

    def __build_time_sheet_schema(self):
        self.time_sheets = Table(
            'time_sheets', self.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('year', Integer, index=True, nullable=False),
            Column('month', Integer, nullable=False),
            Column('norm', Integer),
            Column('rate', Integer),
            Column('sheet', ArrayType()),
            Column('vacation', Float(8)),
            Column('employee_id', Integer, ForeignKey('employees.id'), nullable=False),
            Column('closed', Boolean, nullable=False)
        )

    def __map_entities(self):
        clear_mappers()
        mapper(TimeSheet, self.time_sheets)
        mapper(Employee, self.employees, properties={
            'time_sheets': relationship(
                TimeSheet,
                backref='employees_time_sheet',
                foreign_keys=[self.time_sheets.c.employee_id],
            )
        })
