import ezgmail
import sys, os, glob
import requests
from urllib.request import urlopen

from PyQt5 import uic
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QDateEdit, QDialog, QTextEdit

class DownloadThread(QThread):
    
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self) 
        self.photo_list = []

    def run(self):
        
        # GET all photos and save it with whole number names.
        for i in range(len(self.photo_list)):
            if i == 10: # Limit of 10 images
                break

            res = urlopen(self.photo_list[i]['img_src'])
            
            # Succesful response
            if res.getcode() == 200:
                with open(f"images/{i}.png", "wb") as file:
                    # self.setWindowTitle(f"Downloading image {i+1} out of {len(self.photo_list)}")
                    file.write(res.read())

            # Failed GET
            # else:
                # self.setWindowTitle(f"Downloading image {i+1} failed.")
                
        # Emit signal when process is over
        self.signal.emit(res.getcode())

class MailThread(QThread):

    signal = pyqtSignal('PyQt_PyObject')

    def __init(self):
        self.receiver = ""
        self.subject = ""
        self.body = ""

    def run(self):

        count = 0
        dir_path = r'/home/deny/amFOSS/martian/images'
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        # Send mail
        if "," in self.receiver:
            for address in list(self.receiver.split(",")):
                print(address)
                attachments = [f"images/{i}.png" for i in range(count)]
                ezgmail.send(address, self.subject, self.body, attachments)
        else:
            attachments = [f"images/{i}.png" for i in range(count)]
            ezgmail.send(self.receiver, self.subject, self.body, attachments)
        self.signal.emit(self.receiver)

# Main Window        
class UI(QMainWindow):
    
    current_image = 0 # Filename without EXT
    last_image = -1 # Var to save final filename without EXT

    def __init__(self):
        super(UI, self).__init__()

        # Loads UI from file
        uic.loadUi('base.ui', self)

        # Set window title
        self.setWindowTitle("Martian Chronicles")

        # Declares widgets
        self.dropdown = self.findChild(QComboBox, "comboBox")
        self.next_button = self.findChild(QPushButton, "pushButton")
        self.previous_button = self.findChild(QPushButton, "pushButton_2")
        self.fetch_button = self.findChild(QPushButton, "pushButton_4")
        self.mail = self.findChild(QPushButton, "pushButton_3")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.image = self.findChild(QLabel, "label")

        # Set startup image
        self.pixmap = QPixmap(f"default.png")
        self.image.setPixmap(self.pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        # Link buttons with onClick functions
        self.next_button.clicked.connect(self.next)
        self.previous_button.clicked.connect(self.previous)
        self.fetch_button.clicked.connect(self.fetch)
        self.mail.clicked.connect(self.send_mail)
        
        # Threading
        self.dl_thread = DownloadThread()
        self.dl_thread.signal.connect(self.finished)
        self.dl_thread.photo_list = []

       
        self.show()

    # Go to next image 
    def next(self):

        # If last file, go to first file
        if os.path.isfile(f"images/{self.current_image + 1}.png"):
            self.current_image += 1
        else:
            self.current_image = 0 
        
        # Set image and title
        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        self.image.setPixmap(self.pixmap)

        # Use window title as label
        self.setWindowTitle(f"{self.current_image}.png")
    
    # Go to previous image
    def previous(self):

        # If first file, go to last file
        if os.path.isfile(f"images/{self.current_image - 1}.png"):
            self.current_image -= 1
        else:
            self.current_image = self.last_image
 
        # Set image and title
        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        self.image.setPixmap(self.pixmap)

        # Use window title as label 
        self.setWindowTitle(f"{self.current_image}.png")
    
    # Fetch images from API, run on separate thread
    def fetch(self):

        # Disable all other buttons while fetching
        self.fetch_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.previous_button.setEnabled(False)
        self.mail.setEnabled(False)
        self.date.setEnabled(False)
        self.dropdown.setEnabled(False)

        # Remove all files in images/
        files = glob.glob('images/*')
        for f in files:
            os.remove(f)
            
        # ENV variable
        API_KEY = os.getenv("NASAKEY")

        # Construct request
        base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
        
        rover = self.dropdown.currentText()

        datetimeDate = self.date.date().toPyDate()
        date = datetimeDate.strftime('%Y-%m-%d')

        url = base_url + rover.lower() + "/photos?"
        parameters = {
            "earth_date": date,
            "api_key": "gGSfhfS9Gn1YO4eSz1bgDaqVf6K0Fkbv7T6K2aOx"
        }

        # Send GET request and get list of photo elements 
        response = requests.get(url, params=parameters)
        # Show error if response.status_code is not 2xx
        if list(str(response.status_code))[0] != "2":
            self.fetch_button.setEnabled(True)
            self.next_button.setEnabled(True)
            self.previous_button.setEnabled(True)
            self.mail.setEnabled(True)
            self.date.setEnabled(True)
            self.dropdown.setEnabled(True)
            
            server_error_dlg = ServerErrorDialog()
            server_error_dlg.exec()

            return

        # Show error if there are no photos on given date            
        elif response.json()['photos'] == []:
            self.fetch_button.setEnabled(True) 
            self.next_button.setEnabled(True)
            self.previous_button.setEnabled(True)
            self.mail.setEnabled(True)
            self.date.setEnabled(True)
            self.dropdown.setEnabled(True)

            no_photos_dlg = PhotoErrorDialog()
            no_photos_dlg.exec()

            return
        
        # Threading
        self.dl_thread.photo_list = response.json()['photos']
        self.last_image = len(self.dl_thread.photo_list) - 1
        if self.last_image > 9:
            self.last_image = 9
        self.setWindowTitle('Downloading Images...')
        self.dl_thread.start()


    # Executed once @fetch is done.
    def finished(self, result):
        
        # Display first image
        self.pixmap = QPixmap(f"images/0.png")
        self.image.setPixmap(self.pixmap)
        self.setWindowTitle(f"0.png")

        # Re-enable all buttons once images are fetched 
        self.fetch_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.previous_button.setEnabled(True)
        self.mail.setEnabled(True)
        self.date.setEnabled(True)
        self.dropdown.setEnabled(True)

    # Open window for email
    def send_mail(self):
        dlg = MailDialog(self)
        dlg.exec()

        self.setWindowTitle(f"Mail sent!")

# Mail window
class MailDialog(QDialog):



    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('mail.ui', self)

        # Declares widgets
        self.to_field = self.findChild(QTextEdit, "textEdit")
        self.subject_field = self.findChild(QTextEdit, "textEdit_3")
        self.body_field = self.findChild(QTextEdit, "textEdit_2")
        self.send_mail = self.findChild(QPushButton, "pushButton")
        self.cancel = self.findChild(QPushButton, "pushButton_2")

        # onClick
        self.send_mail.clicked.connect(self.send)
        self.cancel.clicked.connect(lambda:self.close())

        self.mail_thread = MailThread()
        self.mail_thread.signal.connect(self.sent)

        self.setWindowTitle(f"Mail")


    # Sends mail        
    def send(self):
        
        self.send_mail.setEnabled(False)
        self.cancel.setEnabled(False)
        self.to_field.setEnabled(False)
        self.subject_field.setEnabled(False)
        self.body_field.setEnabled(False)
        self.setWindowTitle("Sending mail...")
        # Get input from text fields
        receiver = self.to_field.toPlainText()
        subject = self.subject_field.toPlainText()
        body = self.body_field.toPlainText()

        self.mail_thread.receiver = receiver
        self.mail_thread.subject = subject
        self.mail_thread.body = body
        self.mail_thread.start()

    def sent(self, result):
        self.close()

# Dialog box for API error
class ServerErrorDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('server_error.ui', self)
    
        # Declares widgets
        self.ok_button = self.findChild(QPushButton, "pushButton")

        # onClick
        self.ok_button.clicked.connect(lambda:self.close())

# Dialog box for no photos returned
class PhotoErrorDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('no_photos.ui', self)

        # Declares widgets
        self.ok_button = self.findChild(QPushButton, "pushButton")

        # onClick
        self.ok_button.clicked.connect(lambda:self.close())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

#* Dates with images and dates without
# With:
# Curiosity 03-06-2015 (NO Spirit)
#           03-07-2015
# 