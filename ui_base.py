# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'base.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFrame, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1009, 858)
        self.actioneven_more_stuff = QAction(MainWindow)
        self.actioneven_more_stuff.setObjectName(u"actioneven_more_stuff")
        self.actionChange_Rover = QAction(MainWindow)
        self.actionChange_Rover.setObjectName(u"actionChange_Rover")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(-10, 750, 1041, 80))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(810, 20, 89, 25))
        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(910, 20, 89, 25))
        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(160, 20, 89, 25))
        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(680, 20, 89, 25))
        self.dateEdit = QDateEdit(self.frame)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(30, 20, 110, 26))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 1011, 751))
        self.label.setMinimumSize(QSize(1011, 751))
        self.label.setMaximumSize(QSize(1011, 751))
        self.label.setPixmap(QPixmap(u"images/FLB_486615455EDR_F0481570FHAZ00323M_.jpeg"))
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setMargin(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.label.raise_()
        self.frame.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1009, 22))
        self.menustUFF = QMenu(self.menubar)
        self.menustUFF.setObjectName(u"menustUFF")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menustUFF.menuAction())
        self.menustUFF.addAction(self.actioneven_more_stuff)
        self.menustUFF.addAction(self.actionChange_Rover)

        self.retranslateUi(MainWindow)
        self.pushButton_4.clicked.connect(self.pushButton_4.show)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"hmm yes surely it won't crash this time", None))
        self.actioneven_more_stuff.setText(QCoreApplication.translate("MainWindow", u"Change Date", None))
        self.actionChange_Rover.setText(QCoreApplication.translate("MainWindow", u"Change Rover", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Fetch", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Mail", None))
        self.label.setText("")
        self.menustUFF.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

