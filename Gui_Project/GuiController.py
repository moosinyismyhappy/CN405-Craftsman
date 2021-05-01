import time
import sys
import threading
from threading import Thread
from PyQt5 import QtGui, QtWidgets, Qt, QtCore
from PyQt5.QtGui import QMouseEvent, QPixmap

from Gui_Project.GuiColorDetection import GuiColorDetection
from Gui_Project.GuiImageStorage import GuiImageStorage
from Gui_Project.GuiInputVideo import GuiInputVideo
from Gui_Project.GuiLayout import Ui_MainWindow
from Gui_Project.GuiOutputVideo import GuiOutputVideo


class GuiController(Thread):
    def __init__(self):
        super().__init__()
        self.image_storage = GuiImageStorage()
        self.thread_input_video = None
        self.thread_output_video = None
        self.count = 0
        self.is_first_left_click = True
        self.is_first_right_click = True
        self.show_tracking_toggle_status = True

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)

        # Setting widget event
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.open_camera_button)
        self.ui.pushButton_2.clicked.connect(self.close_camera_button)
        self.ui.pushButton_3.clicked.connect(self.change_to_setting_page)
        self.ui.pushButton_4.clicked.connect(self.change_to_main_page)
        self.ui.pushButton_5.clicked.connect(self.exit_button)
        self.ui.pushButton_6.clicked.connect(self.change_showing_image_to_rgb)
        self.ui.pushButton_7.clicked.connect(self.change_showing_image_to_gray)
        self.ui.pushButton_8.clicked.connect(self.change_showing_image_to_hsv)
        self.ui.pushButton_9.clicked.connect(self.show_tracking)
        self.ui.label_5.setVisible(False)
        self.ui.label_5.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.ui.label_7.setVisible(False)
        self.ui.label_6.setText("Camera is close")
        self.ui.label.mousePressEvent = self.get_position_from_image
        self.ui.label.setVisible(False)

        MainWindow.show()
        sys.exit(app.exec_())

    def show_tracking(self):
        if self.show_tracking_toggle_status:
            self.ui.label_5.setVisible(True)
            self.ui.label_7.setText("Show Tracking")
            self.ui.label_7.setVisible(True)
            pixmap = QPixmap('../resources/images/transparent1.png')
            self.ui.label_5.setPixmap(pixmap)
            self.show_tracking_toggle_status = False
        else:
            self.ui.label_5.setVisible(False)
            self.ui.label_7.setText("")
            self.ui.label_7.setVisible(False)
            self.show_tracking_toggle_status = True


    def change_showing_image_to_rgb(self):
        self.image_storage.set_show_status(0)
        self.ui.label_6.setText("RGB System")
        self.ui.label_6.setStyleSheet('color: Lime')
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)

    def change_showing_image_to_gray(self):
        self.image_storage.set_show_status(2)
        self.ui.label_6.setText("GRAY System")
        self.ui.label_6.setStyleSheet('color: Lime')
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_6.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)

    def change_showing_image_to_hsv(self):
        self.image_storage.set_show_status(1)
        self.ui.label_6.setText("HSV System")
        self.ui.label_6.setStyleSheet('color: Lime')
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_6.setEnabled(True)
        self.ui.pushButton_7.setEnabled(True)


    def get_position_from_image(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.is_first_left_click:
                self.left_color_detection = GuiColorDetection(self, self.image_storage)
                self.left_color_detection.start()
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.left_color_detection.set_hsv()
                self.is_first_left_click = False
            else:
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.left_color_detection.set_hsv()

        elif event.buttons() == QtCore.Qt.RightButton:
            if self.is_first_right_click:
                self.right_color_detection = GuiColorDetection(self, self.image_storage)
                self.right_color_detection.start()
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.right_color_detection.set_hsv()
                self.is_first_right_click = False
            else:
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.right_color_detection.set_hsv()

    def change_to_main_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def change_to_setting_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def exit_button(self):
        sys.exit(0)

    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        self.ui.label_6.setText("RGB System")
        self.ui.label_6.setStyleSheet('color: Lime')
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)
        self.ui.pushButton_9.setEnabled(True)

        # Setting widget event
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.label.setVisible(True)

        # Create Thread for input_video
        self.thread_input_video = GuiInputVideo(self.image_storage)
        self.thread_input_video.set_camera_status(True)
        self.image_storage.set_storage_status(True)
        self.thread_input_video.start()

        # Create Thread for output_video
        self.thread_output_video = GuiOutputVideo(self, self.image_storage)
        self.thread_output_video.start()

    def draw_image(self, image):
        time.sleep(0.001)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_camera_button(self):
        print('Close Camera Button Clicked...')
        self.ui.label_6.setText("Camera is close")
        self.ui.label_6.setStyleSheet('color: Red')
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_6.setEnabled(False)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.thread_input_video.set_camera_status(False)
        self.image_storage.set_storage_status(False)
        self.ui.label.setVisible(False)
