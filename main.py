from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
import requests
import os
import shutil

class UI(QMainWindow):
    
    current_image = 0 

    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('base.ui', self)

        self.next_button = self.findChild(QPushButton, "pushButton")
        self.previous_button = self.findChild(QPushButton, "pushButton_2")
        self.fetch_button = self.findChild(QPushButton, "pushButton_4")

        self.image = self.findChild(QLabel, "label")

        self.next_button.clicked.connect(self.next)
        self.previous_button.clicked.connect(self.previous)
        self.fetch_button.clicked.connect(self.fetch)
        self.show()

    def next(self):
        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        self.current_image += 1 #!TODO: Check if > max and loop back if true 
        self.image.setPixmap(self.pixmap)
    
    def previous(self):
        self.pixmap = QPixmap(f"images/{self.current_image}.png")
        self.current_image -= 1 #!TODO: Check if < 0 and loop back if true 
        self.image.setPixmap(self.pixmap)

    def fetch(self):

        API_KEY = os.getenv("NASAKEY")

        base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/"
        rover = input("ASdsA: ? ") #TODO: Get from APP
        url = base_url + rover + "/photos?"
        date = input("DATE: ") #TODO: Get from APP

        parameters = {
            "earth_date": date,
            "api_key": API_KEY
        }

        # curiosity works : 2015-6-3
        # while spirt doesn't  

        response = requests.get(url, params=parameters)
        photo_list = response.json()['photos'] #! Handle non positive responses 
        photos = []

        if response.json()['photos'] == []:
            #TODO handle no photos
            pass 
        
        for i in range(len(photo_list)):
            photos.append(photo_list[i]['img_src'])

        for idx, image_url in enumerate(photos):
            res = requests.get(image_url, allow_redirects=True)
            if res.status_code == 200:
                with open(f"images/{idx}.png", "wb") as file:
                    file.write(res.content)
                print(f"{idx} done") #TODO: Display to user
            else:
                print(f"{idx} skipped")

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()