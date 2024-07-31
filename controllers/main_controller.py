from PyQt5.QtWidgets import QMessageBox

from views.main_window import MainWindow
from controllers.api_key_controller import ApiKeyController


class MainController:
    def __init__(self):
        self.main_window = None
        self.api_key_controller = ApiKeyController(self)

    def show_api_key_form(self):
        self.api_key_controller.show_form()

    def show_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.api_key_controller.close_form()

    def show_error(self):
        QMessageBox.critical(self.api_key_controller.api_key_form, 'Error',
                             'Invalid API Key. Please try again.')
        self.api_key_controller.api_key_form.api_key_input.setText('')
