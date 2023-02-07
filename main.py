from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QDateEdit
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys, os, glob
import requests, urllib.request
from urllib.request import urlopen
import ezgmail

class DownloadThread(QThread): #* What?
    
    signal = pyqtSignal('PyQt_PyObject') #* What

    def __init__(self): #* What
        QThread.__init__(self) 
        self.photo_list = []

    def run(self):
        # GET all photos and save it with whole number names.
        for i in range(len(self.photo_list)):
            if i == 10: # Limit of 10 images
                break

            # * what
            res = urlopen(self.photo_list[i]['img_src'])
            
            # Succesful response
            if res.getcode() == 200:

                with open(f"images/{i}.png", "wb") as file:
                    file.write(res.read())
                    #TODO: (maybe) implement progress bar

            # Failed GET
            else:
                print(f"{i} skipped") #TODO: (maybe) display to user
        
        # Emit signal when process is over
        self.signal.emit(res.getcode())
        
class UI(QMainWindow):
    
    current_image = 0 # Filename without EXT
    last_image = -1 # Var to save final filename without EXT

    def __init__(self): # * hmm what?
        super(UI, self).__init__()

        # Loads UI from file
        uic.loadUi('base.ui', self)

        self.setWindowTitle("Martian Chronicles")

        # Declares widgets in order to add functionality to them
        self.dropdown = self.findChild(QComboBox, "comboBox")
        self.next_button = self.findChild(QPushButton, "pushButton")
        self.previous_button = self.findChild(QPushButton, "pushButton_2")
        self.email = self.findChild(QPushButton, "pushButton_3")
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
        
        #* Threading but what
        self.dl_thread = DownloadThread()
        self.dl_thread.signal.connect(self.finished)

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

        self.setWindowTitle(f"{self.current_image}.png")
    
    # Fetch images from API, run on separate thread
    def fetch(self):

        self.fetch_button.setEnabled(False)
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
            "api_key": API_KEY
        }

        # Send GET request and get list of photo elements 
        response = requests.get(url, params=parameters)
        #! Make dialog box to handle non positive responses
        if list(str(response.status_code))[0] != "2":
            print("well well well look how the turns have tabled")
            print(response.text)
            self.fetch_button.setEnabled(True)
            return None

        #* something something threading yes        
        self.dl_thread.photo_list = response.json()['photos']
        self.last_image = len(self.dl_thread.photo_list) - 1
        self.dl_thread.start()
        
        # TODO: Make dialog box to handle days where there are no photos taken
        # if response.json()['photos'] == []:
            # pass

    # Executed once @fetch is done.
    def finished(self, resultx):
        
        # Display first image
        self.pixmap = QPixmap(f"images/0.png")
        self.image.setPixmap(self.pixmap)
        self.fetch_button.setEnabled(True)

    def send_mail(self):
        ezgmail.send('gmailid@gmail.com', 'Subject', 'Body', attachments='default.png', cc='anothergmailid@gmail.com' )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()

#* Dates with images and dates without
# With:
# Curiosity 03-06-2015