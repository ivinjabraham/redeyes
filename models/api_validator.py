import time
from PyQt5.QtCore import QThread, pyqtSignal

class ApiValidator(QThread):
    result = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def validate(self, api_key):
        self.api_key = api_key
        self.start()

    def run(self):
        # Simulate an API call with a time delay
        time.sleep(2)
        if self.api_key == "valid_key":
            self.result.emit(True)
        else:
            self.result.emit(False)
