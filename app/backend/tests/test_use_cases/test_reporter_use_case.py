import unittest
from datetime import datetime

import re

from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage
from tests.fake_db import FakeDb
from usecases.reporter_use_case import ReporterUseCase
from utils.excel_reporter import ExcelReporter


class TestProvideEmployeeUseCase(unittest.TestCase):
    def setUp(self):
        db = FakeDb().build()
        self.time_sheet_storage = TimeSheetsStorage(db)
        self.employee_storage = EmployeesStorage(db)
        self.calculator = VacationCalculator()
        reporter = ExcelReporter()
        self.use_case = ReporterUseCase(self.employee_storage,
                                        self.time_sheet_storage,
                                        self.calculator,
                                        reporter)

    def test_get_report_data(self):
        data = self.use_case.get_data(datetime(2018, 1, 1))
        employees = self.employee_storage.find_by(activated=True)
        time_sheets = self.time_sheet_storage.get_all()

        expected_columns_count = 6
        self.assertEqual(data.__len__(), expected_columns_count)

        expected_names = [employee.name for employee in employees]
        self.assertEqual(data['ФИО'], expected_names)
        expected_worked_days = [self.calculator.calculate_days_worked(time_sheet)
                                for time_sheet in time_sheets]
        self.assertEqual(data['Отработано дней'], expected_worked_days)
        expected_norms = [time_sheet.norm for time_sheet in time_sheets]
        self.assertEqual(data['Норма рабочих дней'], expected_norms)
        expected_month_vac = [time_sheet.vacation for time_sheet in time_sheets]
        self.assertEqual(data['Зачислено отпускных дней'], expected_month_vac)
        expected_used_vac = [self.calculator.calculate_used_vacation(time_sheet)
                             for time_sheet in time_sheets]
        self.assertEqual(data['Использовано отпускных дней'], expected_used_vac)
        expected_total_vacation = [employee.vacation for employee in employees]
        self.assertEqual(data['Всего отпускных дней'], expected_total_vacation)

    def test_get_report(self):
        path = self.use_case.get_formed_report_by_date(datetime(2018, 1, 1))
        self.assertTrue(re.match('.*/reports/1.2018.xlsx', path))
