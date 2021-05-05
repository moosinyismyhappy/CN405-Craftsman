# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GuiLayout.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, -3, 1024, 768))
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.pushButton_open_camera = QtWidgets.QPushButton(self.page)
        self.pushButton_open_camera.setGeometry(QtCore.QRect(290, 620, 151, 61))
        self.pushButton_open_camera.setStyleSheet("")
        self.pushButton_open_camera.setObjectName("pushButton_open_camera")
        self.pushButton_stop_camera = QtWidgets.QPushButton(self.page)
        self.pushButton_stop_camera.setGeometry(QtCore.QRect(580, 620, 151, 61))
        self.pushButton_stop_camera.setStyleSheet("")
        self.pushButton_stop_camera.setObjectName("pushButton_stop_camera")
        self.pushButton_show_setting = QtWidgets.QPushButton(self.page)
        self.pushButton_show_setting.setGeometry(QtCore.QRect(790, 700, 101, 41))
        self.pushButton_show_setting.setStyleSheet("background-color: rgb(170, 85, 0);")
        self.pushButton_show_setting.setObjectName("pushButton_show_setting")
        self.widget_place_camera = QtWidgets.QWidget(self.page)
        self.widget_place_camera.setGeometry(QtCore.QRect(180, 80, 661, 501))
        self.widget_place_camera.setStyleSheet("background-color: rgb(229, 231, 255);")
        self.widget_place_camera.setObjectName("widget_place_camera")
        self.label_camera = QtWidgets.QLabel(self.widget_place_camera)
        self.label_camera.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.label_camera.setStyleSheet("")
        self.label_camera.setText("")
        self.label_camera.setObjectName("label_camera")
        self.label_show_tracking = QtWidgets.QLabel(self.widget_place_camera)
        self.label_show_tracking.setGeometry(QtCore.QRect(140, 100, 640, 480))
        self.label_show_tracking.setStyleSheet("")
        self.label_show_tracking.setText("")
        self.label_show_tracking.setObjectName("label_show_tracking")
        self.pushButton_exit = QtWidgets.QPushButton(self.page)
        self.pushButton_exit.setGeometry(QtCore.QRect(910, 700, 101, 41))
        self.pushButton_exit.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_show_rgb = QtWidgets.QPushButton(self.page)
        self.pushButton_show_rgb.setGeometry(QtCore.QRect(10, 190, 151, 61))
        self.pushButton_show_rgb.setStyleSheet("")
        self.pushButton_show_rgb.setObjectName("pushButton_show_rgb")
        self.pushButton_show_gray = QtWidgets.QPushButton(self.page)
        self.pushButton_show_gray.setGeometry(QtCore.QRect(10, 430, 151, 61))
        self.pushButton_show_gray.setStyleSheet("")
        self.pushButton_show_gray.setObjectName("pushButton_show_gray")
        self.pushButton_show_hsv = QtWidgets.QPushButton(self.page)
        self.pushButton_show_hsv.setGeometry(QtCore.QRect(10, 310, 151, 61))
        self.pushButton_show_hsv.setStyleSheet("")
        self.pushButton_show_hsv.setObjectName("pushButton_show_hsv")
        self.pushButton_show_tracking = QtWidgets.QPushButton(self.page)
        self.pushButton_show_tracking.setGeometry(QtCore.QRect(860, 320, 151, 61))
        self.pushButton_show_tracking.setStyleSheet("")
        self.pushButton_show_tracking.setObjectName("pushButton_show_tracking")
        self.label_image_type = QtWidgets.QLabel(self.page)
        self.label_image_type.setGeometry(QtCore.QRect(10, 90, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_image_type.setFont(font)
        self.label_image_type.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_image_type.setObjectName("label_image_type")
        self.label_show_type = QtWidgets.QLabel(self.page)
        self.label_show_type.setGeometry(QtCore.QRect(860, 100, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_show_type.setFont(font)
        self.label_show_type.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_show_type.setObjectName("label_show_type")
        self.pushButton_show_detection = QtWidgets.QPushButton(self.page)
        self.pushButton_show_detection.setGeometry(QtCore.QRect(860, 200, 151, 61))
        self.pushButton_show_detection.setStyleSheet("")
        self.pushButton_show_detection.setObjectName("pushButton_show_detection")
        self.label_show_detection = QtWidgets.QLabel(self.page)
        self.label_show_detection.setGeometry(QtCore.QRect(60, 100, 640, 480))
        self.label_show_detection.setStyleSheet("")
        self.label_show_detection.setText("")
        self.label_show_detection.setObjectName("label_show_detection")
        self.widget_place_camera.raise_()
        self.pushButton_open_camera.raise_()
        self.pushButton_stop_camera.raise_()
        self.pushButton_show_setting.raise_()
        self.pushButton_exit.raise_()
        self.pushButton_show_rgb.raise_()
        self.pushButton_show_gray.raise_()
        self.pushButton_show_hsv.raise_()
        self.pushButton_show_tracking.raise_()
        self.label_image_type.raise_()
        self.label_show_type.raise_()
        self.pushButton_show_detection.raise_()
        self.label_show_detection.raise_()
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_settings = QtWidgets.QLabel(self.page_2)
        self.label_settings.setGeometry(QtCore.QRect(420, 40, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_settings.setFont(font)
        self.label_settings.setObjectName("label_settings")
        self.pushButton_back_to_menu = QtWidgets.QPushButton(self.page_2)
        self.pushButton_back_to_menu.setGeometry(QtCore.QRect(420, 630, 151, 51))
        self.pushButton_back_to_menu.setObjectName("pushButton_back_to_menu")
        self.dial_detect_area = QtWidgets.QDial(self.page_2)
        self.dial_detect_area.setGeometry(QtCore.QRect(700, 330, 131, 151))
        self.dial_detect_area.setObjectName("dial_detect_area")
        self.label_camera_number = QtWidgets.QLabel(self.page_2)
        self.label_camera_number.setGeometry(QtCore.QRect(120, 190, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_camera_number.setFont(font)
        self.label_camera_number.setObjectName("label_camera_number")
        self.lcdNumber_camera_number = QtWidgets.QLCDNumber(self.page_2)
        self.lcdNumber_camera_number.setGeometry(QtCore.QRect(140, 250, 231, 61))
        self.lcdNumber_camera_number.setMode(QtWidgets.QLCDNumber.Bin)
        self.lcdNumber_camera_number.setObjectName("lcdNumber_camera_number")
        self.label_detect_area = QtWidgets.QLabel(self.page_2)
        self.label_detect_area.setGeometry(QtCore.QRect(690, 180, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_detect_area.setFont(font)
        self.label_detect_area.setObjectName("label_detect_area")
        self.lcdNumber_detect_area = QtWidgets.QLCDNumber(self.page_2)
        self.lcdNumber_detect_area.setGeometry(QtCore.QRect(650, 250, 231, 61))
        self.lcdNumber_detect_area.setObjectName("lcdNumber_detect_area")
        self.dial_camera_number = QtWidgets.QDial(self.page_2)
        self.dial_camera_number.setGeometry(QtCore.QRect(180, 320, 131, 151))
        self.dial_camera_number.setObjectName("dial_camera_number")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.dial_detect_area.sliderMoved['int'].connect(self.lcdNumber_detect_area.display)
        self.dial_camera_number.sliderMoved['int'].connect(self.lcdNumber_camera_number.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Craftsman Effectiveness Detection"))
        self.pushButton_open_camera.setText(_translate("MainWindow", "Open Camera"))
        self.pushButton_stop_camera.setText(_translate("MainWindow", "Stop Camera"))
        self.pushButton_show_setting.setText(_translate("MainWindow", "Settings"))
        self.pushButton_exit.setText(_translate("MainWindow", "Exit"))
        self.pushButton_show_rgb.setText(_translate("MainWindow", "RGB Image"))
        self.pushButton_show_gray.setText(_translate("MainWindow", "Gray Scale Image"))
        self.pushButton_show_hsv.setText(_translate("MainWindow", "HSV Image"))
        self.pushButton_show_tracking.setText(_translate("MainWindow", "Show Tracking"))
        self.label_image_type.setText(_translate("MainWindow", "Camera is close"))
        self.label_show_type.setText(_translate("MainWindow", "Not Selected"))
        self.pushButton_show_detection.setText(_translate("MainWindow", "Show Detection"))
        self.label_settings.setText(_translate("MainWindow", "Settings"))
        self.pushButton_back_to_menu.setText(_translate("MainWindow", "Back to Menu"))
        self.label_camera_number.setText(_translate("MainWindow", "Camera Device Number"))
        self.label_detect_area.setText(_translate("MainWindow", "Area to detect"))
