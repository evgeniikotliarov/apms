import falcon


class App(falcon.API):
    def __init__(self):
        super().__init__()
        self.get_employee_use_case = None
        self.get_employees_use_case = None
        self.create_employee_use_case = None
        self.check_employee_use_case = None
        self.check_admin_rights_use_case = None
        self.register_employee_use_case = None
        self.update_employee_use_case = None
        self.admin_rights_employee_use_case = None

        self.get_time_sheet_use_case = None
        self.get_time_sheets_use_case = None
        self.create_time_sheet_use_case = None
        self.update_time_sheet_use_case = None
        self.close_time_sheet_use_case = None

        self.calculate_vacation_use_case = None
