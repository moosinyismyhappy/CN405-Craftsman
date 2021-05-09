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
        self.is_first_click_toggle_detect = 0

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
        self.ui.pushButton_open_camera.clicked.connect(self.open_camera_button)
        self.ui.pushButton_stop_camera.clicked.connect(self.stop_camera_button)
        self.ui.pushButton_show_setting.clicked.connect(self.go_to_setting_page_button)
        self.ui.pushButton_back_to_menu.clicked.connect(self.go_to_main_page_button)
        self.ui.pushButton_exit.clicked.connect(self.exit_button)
        self.ui.pushButton_show_rgb.clicked.connect(self.display_rgb_image_button)
        self.ui.pushButton_show_gray.clicked.connect(self.display_gray_image_button)
        self.ui.pushButton_show_hsv.clicked.connect(self.display_hsv_image_button)
        self.ui.pushButton_show_detection.clicked.connect(self.toggle_display_detect_area)
        self.ui.pushButton_show_tracking.clicked.connect(self.toggle_display_track_area)
        self.ui.label_show_detection.setStyleSheet("background:transparent")
        self.ui.label_show_tracking.setStyleSheet("background:transparent")
        self.ui.label_camera.mousePressEvent = self.get_position_from_image
        self.ui.label_show_detection.setVisible(False)
        self.ui.label_show_tracking.setVisible(False)

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
        if self.is_first_click_toggle_detect == 0:
            self.transparent_image_detect = QtGui.QPixmap('../resources/images/transparent.png')
            self.painter_instance_detect = QtGui.QPainter(self.transparent_image_detect)
            self.pen_rect = QtGui.QPen(QtCore.Qt.cyan)
            self.pen_rect.setWidth(5)
            self.painter_instance_detect.setPen(self.pen_rect)
            self.painter_instance_detect.drawRect(0,100,100,100)
            # set pixmap onto the label widget
            self.ui.label_show_detection.setPixmap(self.transparent_image_detect)
            self.ui.label_show_detection.show()
            self.ui.label_show_detection.setVisible(True)
            self.is_first_click_toggle_detect = 1
        elif self.is_first_click_toggle_detect == 1:
            self.ui.label_show_detection.setVisible(False)
            self.is_first_click_toggle_detect = 2
        elif self.is_first_click_toggle_detect == 2:
            self.ui.label_show_detection.setVisible(True)
            self.is_first_click_toggle_detect = 1

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
        self.ui.label_camera.setPixmap(QtGui.QPixmap.fromImage(receive_image))

    # Receive detected point from other class and display to gui
    def display_to_detection_zone(self,x,y,w,h):
        pass

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
