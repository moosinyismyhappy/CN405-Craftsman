import sys
import threading
import time

from PyQt5 import QtCore, QtWidgets, QtGui
from Gui_Project.GuiColorDetection import GuiColorDetection
from Gui_Project.GuiImageStorage import GuiImageStorage
from Gui_Project.GuiInputVideo import GuiInputVideo
from Gui_Project.GuiLayout import Ui_MainWindow
from Gui_Project.GuiOutputVideo import GuiOutputVideo


class GuiController(threading.Thread):
    def __init__(self):
        super().__init__()
        # declare instance variable for access other class
        self.image_storage = GuiImageStorage()
        self.thread_input_video = None
        self.thread_output_video = None

        # other instance variable for process
        self.is_first_left_click = True
        self.is_first_right_click = True
        self.tracking_toggle_status = True
        self.detection_toggle_status = True
        self.show_image_type = 0

        # instance for toggle detect
        self.transparent_image_detect = None
        self.painter_instance_detect = None
        self.pen_rect = None

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # run code below with new thread
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)
        self.widget_setting()
        MainWindow.show()
        sys.exit(app.exec_())

    def widget_setting(self):
        # Setting widget and event
        self.ui.open_camera_button.clicked.connect(self.open_camera_button)
        self.ui.setting_button.clicked.connect(self.go_to_setting_page_button)
        self.ui.back_to_main_button.clicked.connect(self.go_to_main_page_button)
        self.ui.exit_button.clicked.connect(self.exit_button)
        self.ui.display_rgb_image_button.clicked.connect(self.display_rgb_image_button)
        self.ui.display_gray_image_button.clicked.connect(self.display_gray_image_button)
        self.ui.display_hsv_image_button.clicked.connect(self.display_hsv_image_button)
        self.ui.display_detect_button.clicked.connect(self.toggle_display_detect_area)
        self.ui.display_track_button.clicked.connect(self.toggle_display_track_area)
        self.ui.display_detect_frame.setStyleSheet("background:transparent")
        self.ui.display_track_frame.setStyleSheet("background:transparent")
        self.ui.display_camera_frame.mousePressEvent = self.get_position_from_image

    # RGB Image Button
    def display_rgb_image_button(self):
        print('display rgb')
        self.set_show_image_type(0)

    # HSV Image Button
    def display_hsv_image_button(self):
        print('display hsv')
        self.set_show_image_type(1)

    # GrayScale Image Button
    def display_gray_image_button(self):
        print('display gray')
        self.set_show_image_type(2)

    # Toggle display detected area Button
    def toggle_display_detect_area(self):
        print('toggle display detect area')

    # Receive detected point from other class and display to gui
    def display_to_detection_zone(self):
        pass

    # Toggle display track area Button
    def toggle_display_track_area(self):
        print('toggle display track area')

    # Open Camera Button
    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        # Create Thread for input_video
        self.thread_input_video = GuiInputVideo(self.image_storage)
        self.thread_input_video.start()

        # Create Thread for output_video
        self.thread_output_video = GuiOutputVideo(self, self.image_storage)
        self.thread_output_video.start()

    # Stop Camera Button
    def stop_camera_button(self):
        print('Stop Camera Button Clicked...')

    # Exit program Button
    def exit_button(self):
        print('Exit Button Clicked...')
        sys.exit(0)

    # Go to setting page from main page button
    def go_to_setting_page_button(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    # Back to main page from setting page button
    def go_to_main_page_button(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # Receive image from other class and display to gui
    def display_image_to_camera_zone(self, receive_image):
        time.sleep(0.001)
        self.ui.display_camera_frame.setPixmap(QtGui.QPixmap.fromImage(receive_image))


    # Receive track point from other class and display to gui
    def display_to_tracking_zone(self,x,y):
        pass

    # Set which type of image (RGB,HSV,GRAYSCALE)
    def set_show_image_type(self, new_type):
        self.show_image_type = new_type

    def get_show_image_type(self):
        return self.show_image_type

    # Get x,y from mouse clicked method
    def get_position_from_image(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.is_first_left_click:
                print('First click from Left', event.pos().x(), event.pos().y())
                self.left_color_detection = GuiColorDetection(self, self.image_storage)
                self.left_color_detection.start()
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.left_color_detection.set_hsv()
                self.is_first_left_click = False
            else:
                print('click from Left', event.pos().x(), event.pos().y())
                self.left_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.left_color_detection.set_hsv()

        elif event.buttons() == QtCore.Qt.RightButton:
            if self.is_first_right_click:
                print('First click from Right', event.pos().x(), event.pos().y())
                self.right_color_detection = GuiColorDetection(self, self.image_storage)
                self.right_color_detection.start()
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.right_color_detection.set_hsv()
                self.is_first_right_click = False
            else:
                print('click from Right', event.pos().x(), event.pos().y())
                self.right_color_detection.set_pos(event.pos().x(), event.pos().y())
                self.right_color_detection.set_hsv()
