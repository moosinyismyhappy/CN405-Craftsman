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
        self.stackedWidget.setGeometry(QtCore.QRect(10, 10, 1001, 721))
        self.stackedWidget.setStyleSheet("background-color: rgb(188, 188, 188);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(200, 70, 640, 480))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setGeometry(QtCore.QRect(250, 590, 151, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.page)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 590, 151, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.page)
        self.pushButton_3.setGeometry(QtCore.QRect(640, 590, 151, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setGeometry(QtCore.QRect(190, 60, 661, 501))
        self.widget.setStyleSheet("background-color: rgb(63, 63, 63);")
        self.widget.setObjectName("widget")
        self.pushButton_5 = QtWidgets.QPushButton(self.page)
        self.pushButton_5.setGeometry(QtCore.QRect(930, 0, 71, 21))
        self.pushButton_5.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.page)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 150, 151, 61))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.page)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 240, 151, 61))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.page)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 330, 151, 61))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.page)
        self.pushButton_9.setGeometry(QtCore.QRect(20, 420, 151, 61))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_6 = QtWidgets.QLabel(self.page)
        self.label_6.setGeometry(QtCore.QRect(440, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.page)
        self.label_5.setGeometry(QtCore.QRect(200, 70, 640, 480))
        self.label_5.setStyleSheet("")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.page)
        self.label_7.setGeometry(QtCore.QRect(210, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.widget.raise_()
        self.label.raise_()
        self.label_5.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        self.pushButton_9.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(420, 40, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 630, 151, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.dial = QtWidgets.QDial(self.page_2)
        self.dial.setGeometry(QtCore.QRect(700, 330, 131, 151))
        self.dial.setObjectName("dial")
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setGeometry(QtCore.QRect(120, 190, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lcdNumber = QtWidgets.QLCDNumber(self.page_2)
        self.lcdNumber.setGeometry(QtCore.QRect(140, 250, 231, 61))
        self.lcdNumber.setMode(QtWidgets.QLCDNumber.Bin)
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setGeometry(QtCore.QRect(690, 180, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.page_2)
        self.lcdNumber_2.setGeometry(QtCore.QRect(650, 250, 231, 61))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.dial_2 = QtWidgets.QDial(self.page_2)
        self.dial_2.setGeometry(QtCore.QRect(180, 320, 131, 151))
        self.dial_2.setObjectName("dial_2")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.dial.sliderMoved['int'].connect(self.lcdNumber_2.display)
        self.dial_2.sliderMoved['int'].connect(self.lcdNumber.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Craftsman Effectiveness Detection"))
        self.pushButton.setText(_translate("MainWindow", "Open Camera"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop Camera"))
        self.pushButton_3.setText(_translate("MainWindow", "Settings"))
        self.pushButton_5.setText(_translate("MainWindow", "Exit"))
        self.pushButton_6.setText(_translate("MainWindow", "RGB Image"))
        self.pushButton_7.setText(_translate("MainWindow", "Gray Scale Image"))
        self.pushButton_8.setText(_translate("MainWindow", "HSV Image"))
        self.pushButton_9.setText(_translate("MainWindow", "Show Tracking"))
        self.label_6.setText(_translate("MainWindow", "Camera is close"))
        self.label_2.setText(_translate("MainWindow", "Settings"))
        self.pushButton_4.setText(_translate("MainWindow", "Back to Menu"))
        self.label_3.setText(_translate("MainWindow", "Camera Device Number"))
        self.label_4.setText(_translate("MainWindow", "Area to detect"))
