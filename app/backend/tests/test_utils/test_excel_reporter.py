import os
import unittest

from settings import ROOT_APP_PATH
from utils.excel_reporter import ExcelReporter


class TestExcelReporter(unittest.TestCase):
    def setUp(self):
        self.reporter = ExcelReporter()
        self.data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}
        self.report_name = 'test_reporter'
        self.report_path = '{}/reports/{}.xlsx'.format(ROOT_APP_PATH, self.report_name)

    def test_create_report(self):
        self.reporter.save_report(self.data, self.report_name)
        self.assertTrue(os.path.exists(self.report_path))

    def get_report_path(self):
        self.reporter.save_report(self.data, self.report_name)
        report_path_from_reporter = self.reporter.get_report_path(self.report_name)
        self.assertEqual(report_path_from_reporter, self.report_path)

    def tearDown(self):
        os.remove(self.reporter.get_report_path(self.report_name))
