from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class LoadingDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Loading...')
        self.setModal(True)
        layout = QVBoxLayout()
        self.label = QLabel('Please wait, validating API Key...')
        layout.addWidget(self.label)
        self.setLayout(layout)
