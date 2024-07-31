from PyQt5.QtWidgets import QApplication
import sys

from controllers.main_controller import MainController


def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_api_key_form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
