from PyQt5.QtCore import QObject
from views.api_key_form import ApiKeyForm
from views.loading_dialog import LoadingDialog
from models.api_validator import ApiValidator

class ApiKeyController(QObject):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller
        self.api_key_form = None
        self.loading_dialog = None
        self.api_validator = ApiValidator()
        self.api_validator.result.connect(self.handle_api_result)

    def show_form(self):
        self.api_key_form = ApiKeyForm(self.start_loading)
        self.api_key_form.show()

    def start_loading(self, api_key):
        self.loading_dialog = LoadingDialog(self.api_key_form)
        self.loading_dialog.show()
        self.api_validator.validate(api_key)

    def handle_api_result(self, success):
        self.loading_dialog.done(0)
        if success:
            self.main_controller.show_main_window()
        else:
            self.main_controller.show_error()

    def close_form(self):
        if self.api_key_form:
            self.api_key_form.close()
