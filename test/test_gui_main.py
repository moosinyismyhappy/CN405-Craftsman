import sys
import time

import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

from show_track import Ui_MainWindow
from test_gui_video import TestInputVideo


class TestGuiMain():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)
        self.ui.camera_button.clicked.connect(self.open_camera_button)
        self.ui.show_track_button.clicked.connect(self.show_track_button)
        self.ui.track_label.setStyleSheet("background:transparent")

        self.pixmap_image = QtGui.QPixmap('../resources/images/test_transparent.png')
        # create painter instance with pixmap
        self.painterInstance = QtGui.QPainter(self.pixmap_image)
        # set rectangle color and thickness
        self.penCircle = QtGui.QPen(QtCore.Qt.cyan)
        self.penCircle.setWidth(3)
        # draw rectangle on painter
        self.painterInstance.setPen(self.penCircle)

        self.ui.track_label.setVisible(False)
        MainWindow.show()
        sys.exit(app.exec_())

    def show_track_button(self):
        print('Show tracking')
        self.ui.track_label.setVisible(True)
        self.display_image_to_tracking_zone()
        self.draw_circle_in_tracking()

    def draw_circle_in_tracking(self):
        pass

    def display_image_to_tracking_zone(self,x,y):
        self.painterInstance.drawEllipse(x, y, 20, 20)

        # set pixmap onto the label widget
        self.ui.track_label.setPixmap(self.pixmap_image)
        self.ui.track_label.show()

    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        # Create Thread for input_video
        self.thread_input_video = TestInputVideo(self)
        self.thread_input_video.start()

    def display_image_to_camera_zone(self, receive_image):
        time.sleep(0.001)
        self.ui.camera_label.setPixmap(QtGui.QPixmap.fromImage(receive_image))


if __name__ == "__main__":
    gui = TestGuiMain()
