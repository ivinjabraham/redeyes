from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QComboBox, QDateEdit
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import requests
import datetime
import urllib.request
import os
from threading import *

class UI(QMainWindow):
    
    current_image = 0 # Basically filename without EXT
    last_image = -1

    def __init__(self):
        super(UI, self).__init__()

        # Loads UI from file
        uic.loadUi('base.ui', self)

        self.setWindowTitle("Martian Chronicles")

        # Declares buttons and labels
        self.dropdown = self.findChild(QComboBox, "comboBox")
        self.next_button = self.findChild(QPushButton, "pushButton")
        self.previous_button = self.findChild(QPushButton, "pushButton_2")
        self.email = self.findChild(QPushButton, "pushButton_3")
        self.fetch_button = self.findChild(QPushButton, "pushButton_4")
        self.date = self.findChild(QDateEdit, "dateEdit")

        self.image = self.findChild(QLabel, "label")

        self.pixmap = QPixmap(f"default.png")
        self.image.setPixmap(self.pixmap)
        self.image.setAlignment(Qt.AlignCenter)

        # Link buttons with onClick functions
        self.next_button.clicked.connect(self.next)
        self.previous_button.clicked.connect(self.previous)
        self.fetch_button.clicked.connect(self.fetch)
        
        self.show()
    
    # def pog(self):
        # print("oaksd")

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
        url = base_url + rover.lower() + "/photos?"
        datetimeDate = self.date.date().toPyDate()
        date = datetimeDate.strftime('%Y-%m-%d')

        parameters = {
            "earth_date": date,
            "api_key": API_KEY
        }

        # curiosity works : 2015-6-3
        # while spirt doesn't  

        # Send GET request and get list of photo elements 
        response = requests.get(url, params=parameters)
        photo_list = response.json()['photos'] #! Handle non positive responses 

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
                self.last_image += 1
            
            # Failed GET
            else:
                print(f"{i} skipped")
        
        print("hehe yes")


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()