import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_api_key_form()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
