from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QDateEdit
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import requests
import datetime
import urllib.request
import os

class UI(QMainWindow):
    
    current_image = 0 # Basically filename without EXT
    last_image = -1 # Var to save final filename without EXT

    def __init__(self):
        super(UI, self).__init__()

        # Loads UI from file
        uic.loadUi('base.ui', self)

        # TODO: Show image name instead
        self.setWindowTitle("Martian Chronicles")

        # Declares widgets in order to add functionality to them
        self.dropdown = self.findChild(QComboBox, "comboBox")
        self.next_button = self.findChild(QPushButton, "pushButton")
        self.previous_button = self.findChild(QPushButton, "pushButton_2")
        self.email = self.findChild(QPushButton, "pushButton_3")
        self.fetch_button = self.findChild(QPushButton, "pushButton_4")
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
        
        self.show()
    
    # Go to next image 
    def next(self):

        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        
        if os.path.isfile(f"images/{self.current_image + 1}.png"):
            self.current_image += 1
        else:
            self.current_image = 0 
        
        self.image.setPixmap(self.pixmap)
    
    # Go to previous image
    def previous(self):

        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        
        if os.path.isfile(f"images/{self.current_image - 1}.png"):
            self.current_image -= 1
        else:
            self.current_image = self.last_image
 
        self.image.setPixmap(self.pixmap)

    # Fetch images from API
    def fetch(self):
            
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
        #! Handle non positive responses 
        if list(str(response.status_code))[0] != "2":
            return None
                
        photo_list = response.json()['photos']

        # Handles days where there are no photos taken
        if response.json()['photos'] == []:
            #TODO handle no photos
            pass 
        
        # GET all photos and save it with whole number names.
        for i in range(len(photo_list)):
            if i == 10:
                break

            res = urllib.request.urlopen(photo_list[i]['img_src'])
            
            # Succesful response
            if res.getcode() == 200:

                with open(f"images/{i}.png", "wb") as file:
                    file.write(res.read())
                    print(f"{i} done") #TODO: Display to user 

                self.pixmap = QPixmap(f"images/0.png")
                self.image.setPixmap(self.pixmap)

                self.last_image += 1
            
            # Failed GET
            else:
                print(f"{i} skipped") #TODO: (maybe) display to user
        
        print("hehe yes") #TODO: Display to user

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

#* Dates with images and dates without
# With:
# Curiosity 03-06-2015