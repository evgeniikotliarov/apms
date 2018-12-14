from datetime import datetime

from domain.controllers.vacation_calculator import VacationCalculator
from storages.storages import EmployeesStorage, TimeSheetsStorage
from utils.excel_reporter import ExcelReporter


class ReporterUseCase:
    def __init__(self,
                 employee_storage: EmployeesStorage,
                 time_sheet_storage: TimeSheetsStorage,
                 calculator: VacationCalculator,
                 excel_reporter: ExcelReporter):
        self.employee_storage = employee_storage
        self.time_sheet_storage = time_sheet_storage
        self.calculator = calculator
        self.excel_reporter = excel_reporter
        self.employees = None
        self.time_sheets = None

    def get_formed_report_by_date(self, date: datetime):
        data = self.get_data(date)
        name = '{}.{}'.format(date.month, date.year)
        self.excel_reporter.save_report(data, name)
        return self.excel_reporter.get_report_path(name)

    def get_data(self, date):
        self.init_employees()
        self.init_time_sheets(date)
        return {
            'ФИО': self.names,
            'Отработано дней': self.worked_days,
            'Норма рабочих дней': self.month_norms,
            'Зачислено отпускных дней': self.month_vacations,
            'Использовано отпускных дней': self.used_vacations,
            'Всего отпускных дней': self.total_vacations
        }

    def init_employees(self):
        self.employees = self.employee_storage.find_by(activated=True)
        self._init_columns_data_by_employees()

    def init_time_sheets(self, date):
        self.time_sheets = list(map(lambda employee:
                                    self.time_sheet_storage.find_first_by(employee_id=employee.id,
                                                                          year=date.year,
                                                                          month=date.month),
                                    self.employees))
        self._init_columns_data_by_time_sheets()

    def get_nums(self):
        employee_count = range(1, self.employees.__len__() + 1)
        return list(map(lambda index: index, employee_count))

    def _init_columns_data_by_employees(self):
        self.names = []
        self.total_vacations = []
        for employee in self.employees:
            self.names.append(employee.name)
            self.total_vacations.append(employee.vacation)

    def _init_columns_data_by_time_sheets(self):
        self.month_norms = []
        self.worked_days = []
        self.month_vacations = []
        self.used_vacations = []
        for time_sheet in self.time_sheets:
            self.month_norms.append(time_sheet.norm)
            work_days = self.calculator.calculate_days_worked(time_sheet)
            self.worked_days.append(work_days)
            self.month_vacations.append(time_sheet.vacation)
            used_vacation = self.calculator.calculate_used_vacation(time_sheet)
            self.used_vacations.append(used_vacation)
