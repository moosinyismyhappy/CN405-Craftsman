import time
import sys
import threading
from threading import Thread
from PyQt5 import QtGui, QtWidgets, Qt, QtCore
from PyQt5.QtGui import QMouseEvent

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

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)

        # Setting widget event
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.open_camera_button)
        self.ui.pushButton_2.clicked.connect(self.close_camera_button)
        self.ui.pushButton_3.clicked.connect(self.change_to_setting_page)
        self.ui.pushButton_4.clicked.connect(self.change_to_main_page)
        self.ui.pushButton_5.clicked.connect(self.exit_button)
        self.ui.label.mousePressEvent = self.get_position_from_image
        self.ui.label.setVisible(False)

        MainWindow.show()
        sys.exit(app.exec_())

    def get_position_from_image(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.is_first_left_click:
                print('First Left Click')
                self.left_color_detection = GuiColorDetection(self, self.image_storage)
                self.left_color_detection.start()
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.is_first_left_click = False
            else:
                print('Left Click')
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
        elif event.buttons() == QtCore.Qt.RightButton:
            if self.is_first_right_click:
                print('First Right Click')
                self.right_color_detection = GuiColorDetection(self, self.image_storage)
                self.right_color_detection.start()
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.is_first_right_click = False
            else:
                print('Right Click')
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())

    def change_to_main_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def change_to_setting_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def exit_button(self):
        sys.exit(0)

    def open_camera_button(self):
        print('Open Camera Button Clicked...')

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
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)
        self.thread_input_video.set_camera_status(False)
        self.image_storage.set_storage_status(False)
        self.ui.label.setVisible(False)
