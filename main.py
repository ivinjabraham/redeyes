import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QLineEdit, QFormLayout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


class APIKeyDialog(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('API Key Dialog')
        self.resize(120, 120)

        layout = QFormLayout()

        self.key_field = QLineEdit()
        self.key_field.setEchoMode(QLineEdit.Password)
        layout.addRow("API Key:", self.key_field)

        button_login = QPushButton('Continue')
        button_login.clicked.connect(self.check_key)
        layout.addWidget(button_login)

        self.setLayout(layout)

    def check_key(self):
        if self.key_field.text() == "yes":
            self.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Check for cached API Key in files
    # To set default value
    signed_in = False

    if not signed_in:
        form = APIKeyDialog()
        form.show()

    sys.exit(app.exec_())
