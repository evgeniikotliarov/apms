import os

import pandas

from settings import ROOT_APP_PATH


class ExcelReporter:
    def save_report(self, data, name):
        data_frame = pandas.DataFrame(data)
        writer = pandas.ExcelWriter(self._get_report_path(name), engine='xlsxwriter')
        data_frame.to_excel(writer, sheet_name=name, columns=data.keys())
        writer.save()

    def get_report_path(self, name):
        return self._get_report_path(name)

    def _get_report_path(self, name):
        folder_path = self._get_reports_path()
        return '{}/{}.xlsx'.format(folder_path, name)

    @classmethod
    def _get_reports_path(cls):
        path_to_reports_folder = '{}/reports'.format(ROOT_APP_PATH)
        if not os.path.exists(path_to_reports_folder):
            os.makedirs(path_to_reports_folder)
        return path_to_reports_folder
