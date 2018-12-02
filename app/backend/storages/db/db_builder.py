from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float, Boolean, \
    create_engine, DateTime
# DateTime,
from sqlalchemy.orm import sessionmaker, mapper, relationship

import settings
from domain.models.employee import Employee
from domain.models.time_sheet import TimeSheet


class DbBuilder:
    def __init__(self):
        self.session = None
        self.engine = None
        self.metadata = None
        self.employees = None
        self.time_sheets = None

    def build(self):
        self.metadata = MetaData()
        self.create_session()
        self.create_schema()
        return self.session

    def create_session(self):
        if self.session is None:
            session = sessionmaker(self._create_engine())
            self.session = session()
        return self.session

    def _create_engine(self):
        if self.engine is None:
            self.engine = create_engine(settings.DB_CONNECTION_STRING)
            self.metadata.create_all(self.engine)
        return self.engine

    def create_schema(self):
        self.__build_employee_schema()
        self.__build_time_sheet_schema()
        mapper(Employee, self.employees)
        mapper(TimeSheet, self.time_sheets, properties={
            'employees': relationship(Employee, backref='employee', order_by=self.employees.c.id)
        })

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
            Column('registration_date', DateTime, nullable=True)
        )

    def __build_time_sheet_schema(self):
        self.time_sheets = Table(
            'time_sheets', self.metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('year', Integer, index=True, nullable=False),
            Column('month', Integer, nullable=False),
            Column('norm', Integer, unique=True, nullable=False),
            Column('rate', Integer, nullable=False),
            Column('sheet', String(128), nullable=False),  # TODO !
            Column('vacation', Float(8), nullable=False),
            Column('employee_id', Integer, ForeignKey('employees.id')),
            Column('closed', Boolean, nullable=False)
        )
