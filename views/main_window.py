from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        label = QLabel('Welcome to the main application!', self)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)
