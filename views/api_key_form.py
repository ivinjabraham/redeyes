from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ApiKeyForm(QWidget):
    def __init__(self, submit_callback, parent=None):
        super().__init__(parent)
        self.submit_callback = submit_callback
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('API Key Form')
        layout = QVBoxLayout()

        self.label = QLabel('API Key:')
        layout.addWidget(self.label)

        self.api_key_input = QLineEdit()
        layout.addWidget(self.api_key_input)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit(self):
        api_key = self.api_key_input.text()
        self.submit_callback(api_key)
