import sys
import threading
import time

from PyQt5 import QtCore, QtWidgets, QtGui
from Gui_Project.GuiColorDetection import GuiColorDetection
from Gui_Project.GuiImageStorage import GuiImageStorage
from Gui_Project.GuiInputVideo import GuiInputVideo
from Gui_Project.GuiLayout import Ui_MainWindow
from Gui_Project.GuiProcessOutput import GuiProcessOutput


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
        self.toggle_track_status = 0
        self.toggle_mark_area_status = 0
        self.toggle_detect_status = False
        self.show_image_type = 0
        self.left_or_right_color = -1
        self.mark_area_status = -1


        # draw instance
        self.transparent_image_detect = None
        self.painter_instance = None

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # run code below with new thread
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)
        self.widget_setting()
        self.draw_instance()
        MainWindow.show()
        sys.exit(app.exec_())

    def draw_instance(self):
        # Transparent image Location
        self.image_file = '../resources/images/test_transparent.png'
        # convert image file into pixmap
        self.transparent_image_detect = QtGui.QPixmap(self.image_file)
        # create painter instance with pixmap
        self.painter_instance = QtGui.QPainter(self.transparent_image_detect)

    def widget_setting(self):
        # Setting widget and event
        self.ui.open_camera_button.clicked.connect(self.open_camera_button)
        self.ui.setting_button.clicked.connect(self.go_to_setting_page_button)
        self.ui.back_to_main_button.clicked.connect(self.go_to_main_page_button)
        self.ui.exit_button.clicked.connect(self.exit_button)
        self.ui.select_left_color_button.clicked.connect(self.select_left_color_button)
        self.ui.select_right_color_button.clicked.connect(self.select_right_color_button)
        self.ui.display_rgb_image_button.clicked.connect(self.display_rgb_image_button)
        self.ui.display_hsv_image_button.clicked.connect(self.display_hsv_image_button)
        self.ui.display_gray_image_button.clicked.connect(self.display_gray_image_button)
        self.ui.display_mark_button.clicked.connect(self.toggle_display_mark_area_frame_button)
        self.ui.display_track_button.clicked.connect(self.toggle_display_track_frame_button)
        self.ui.display_detect_button.clicked.connect(self.toggle_display_detect_frame_button)
        self.ui.mark_input_button.clicked.connect(self.mark_input_button)
        self.ui.mark_output_button.clicked.connect(self.mark_output_button)
        self.ui.mark_working_button.clicked.connect(self.mark_working_button)
        self.ui.display_mark_area_frame.setStyleSheet("background:transparent")
        self.ui.display_camera_frame.mousePressEvent = self.get_position_from_camera_frame
        self.ui.display_mark_area_frame.mousePressEvent = self.get_position_from_mark_area_frame
        self.ui.display_mark_area_frame.setVisible(False)
        self.ui.mark_input_button.setEnabled(False)
        self.ui.mark_output_button.setEnabled(False)
        self.ui.mark_working_button.setEnabled(False)
        self.ui.undo_button.setEnabled(False)

    def toggle_display_mark_area_frame_button(self):
        if self.toggle_mark_area_status == 0:
            self.ui.display_mark_area_frame.setVisible(True)
            self.ui.mark_input_button.setEnabled(True)
            self.ui.mark_output_button.setEnabled(True)
            self.ui.mark_working_button.setEnabled(True)
            self.ui.undo_button.setEnabled(True)
            self.toggle_mark_area_status = 1

        elif self.toggle_mark_area_status == 1:
            self.ui.display_mark_area_frame.setVisible(False)
            self.ui.mark_input_button.setEnabled(False)
            self.ui.mark_output_button.setEnabled(False)
            self.ui.mark_working_button.setEnabled(False)
            self.ui.undo_button.setEnabled(False)
            self.toggle_mark_area_status = 0

    def mark_input_button(self):
        print('mark input')
        self.mark_area_status = 0

    def mark_output_button(self):
        print('mark output')
        self.mark_area_status = 1

    def mark_working_button(self):
        self.mark_area_status = 2

    def draw_mark_area(self, x, y):
        if self.mark_area_status == 0:
            # set point color and thickness
            self.pen_point = QtGui.QPen(QtCore.Qt.red)
            self.pen_point.setWidth(3)
            # draw rectangle on painter
            self.painter_instance.setPen(self.pen_point)
            self.painter_instance.drawPoint(x, y)
            self.painter_instance.drawText(x - 10, y - 10, 'Input area')
            # set pixmap onto the label widget
            self.ui.display_mark_area_frame.setPixmap(self.transparent_image_detect)

        elif self.mark_area_status == 1:
            # set point color and thickness
            self.pen_point = QtGui.QPen(QtCore.Qt.green)
            self.pen_point.setWidth(3)
            # draw rectangle on painter
            self.painter_instance.setPen(self.pen_point)
            self.painter_instance.drawPoint(x, y)
            self.painter_instance.drawText(x - 10, y - 10, 'Output area')
            # set pixmap onto the label widget
            self.ui.display_mark_area_frame.setPixmap(self.transparent_image_detect)
        elif self.mark_area_status == 2:
            # set point color and thickness
            self.pen_point = QtGui.QPen(QtCore.Qt.yellow)
            self.pen_point.setWidth(3)
            # draw rectangle on painter
            self.painter_instance.setPen(self.pen_point)
            self.painter_instance.drawPoint(x, y)
            self.painter_instance.drawText(x - 10, y - 10, 'Working area')
            # set pixmap onto the label widget
            self.ui.display_mark_area_frame.setPixmap(self.transparent_image_detect)

    # Select Left Color Button
    def select_left_color_button(self):
        self.left_or_right_color = 0

    # Select Right Color Button
    def select_right_color_button(self):
        print('select right color')
        self.left_or_right_color = 1

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

    # Set which type of image (RGB,HSV,GRAYSCALE)
    def set_show_image_type(self, new_type):
        self.show_image_type = new_type

    def get_show_image_type(self):
        return self.show_image_type

    # Toggle display detect area Button
    def toggle_display_detect_frame_button(self):
        if self.toggle_detect_status:
            self.ui.text_detect.setText('Detection is on')
            self.ui.text_detect.setStyleSheet('color:lime')
            self.toggle_detect_status = False
        else:
            self.ui.text_detect.setText('Detection is off')
            self.ui.text_detect.setStyleSheet('color:red')
            self.toggle_detect_status = True

    def get_toggle_detect_status(self):
        return self.toggle_detect_status

    # Toggle display track area Button
    def toggle_display_track_frame_button(self):
        print('toggle display track area')

    # Open Camera Button
    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        self.ui.text_image_type.setText('RGB Mode')
        # Create Thread for input_video
        self.thread_input_video = GuiInputVideo(self.image_storage)
        self.thread_input_video.start()

        # Create Thread for output_video
        self.thread_output_video = GuiProcessOutput(self, self.image_storage)
        self.thread_output_video.start()

        # Disable button
        self.ui.open_camera_button.setEnabled(False)

    # Receive image from other class and display to gui
    def display_image_to_camera_zone(self, receive_image):
        time.sleep(0.000001)
        self.ui.display_camera_frame.setPixmap(QtGui.QPixmap.fromImage(receive_image))

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

    # Get x,y from mouse clicked method
    def get_position_from_camera_frame(self, event):
        x_position = event.pos().x()
        y_position = event.pos().y()
        # check which select color button is pressed
        # select left color button is pressed
        if self.left_or_right_color == 0:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                # first click will be start thread once
                if self.is_first_left_click:
                    self.left_color_detection = GuiColorDetection(self, self.image_storage)
                    self.left_color_detection.start()
                    self.left_color_detection.set_position(x_position, y_position)
                    self.left_color_detection.set_hsv()
                    self.is_first_left_click = False
                # set new color without start thread
                else:
                    self.left_color_detection.set_position(x_position, y_position)
                    self.left_color_detection.set_hsv()

        # select right color button is pressed
        elif self.left_or_right_color == 1:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                # first click will be start thread once
                if self.is_first_right_click:
                    self.right_color_detection = GuiColorDetection(self, self.image_storage)
                    self.right_color_detection.start()
                    self.right_color_detection.set_position(x_position, y_position)
                    self.right_color_detection.set_hsv()
                    self.is_first_right_click = False
                # set new color without start thread
                else:
                    self.right_color_detection.set_position(x_position, y_position)
                    self.right_color_detection.set_hsv()

        # set state to -1 to not allow select color without select color button
        self.left_or_right_color = -1

    def get_position_from_mark_area_frame(self, event):
        x_position = event.pos().x()
        y_position = event.pos().y()
        if self.mark_area_status == 0:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                self.draw_mark_area(x_position, y_position)

        elif self.mark_area_status == 1:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                print('mark output')
                self.draw_mark_area(x_position, y_position)

        elif self.mark_area_status == 2:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                self.draw_mark_area(x_position, y_position)

        # set state to -1 restate of select area
        self.mark_area_status = -1
