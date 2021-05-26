import sys
import threading
import time

import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QPixmap

from Gui_Project.GuiCalibrate import GuiCalibrate
from Gui_Project.GuiColorDetection import GuiColorDetection
from Gui_Project.GuiImageStorage import GuiImageStorage
from Gui_Project.GuiInputVideo import GuiInputVideo
from Gui_Project.GuiLayout import Ui_MainWindow
from Gui_Project.GuiProcessOutput import GuiProcessOutput
from Gui_Project.GuiTimer import GuiTimer


class GuiController(threading.Thread):
    def __init__(self):
        super().__init__()
        # declare instance variable for access other class
        self.image_storage = GuiImageStorage()
        self.calibrate = GuiCalibrate()
        self.timer = None
        self.thread_input_video = None
        self.thread_output_video = None

        # other instance variable for process
        self.is_first_left_click = True
        self.is_first_right_click = True
        self.toggle_track_status = False
        self.toggle_mark_area_status = False
        self.toggle_detect_status = False
        self.toggle_calibrate_status = False
        self.is_calibrate = False
        self.show_image_type = 0
        self.left_or_right_color = -1
        self.which_marked_area = -1


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
        # setting button to call function
        self.ui.open_camera_button.clicked.connect(self.open_camera_button)
        self.ui.setting_button.clicked.connect(self.go_to_setting_button)
        self.ui.back_to_main_button.clicked.connect(self.go_to_main_button)
        self.ui.exit_button.clicked.connect(self.exit_button)
        self.ui.select_left_color_button.clicked.connect(self.select_left_color_button)
        self.ui.select_right_color_button.clicked.connect(self.select_right_color_button)
        self.ui.display_rgb_image_button.clicked.connect(self.display_rgb_image_button)
        self.ui.display_hsv_image_button.clicked.connect(self.display_hsv_image_button)
        self.ui.display_gray_image_button.clicked.connect(self.display_gray_image_button)
        self.ui.display_mark_button.clicked.connect(self.toggle_display_mark_area)
        self.ui.display_track_button.clicked.connect(self.toggle_display_track_button)
        self.ui.display_detect_button.clicked.connect(self.toggle_display_detect_button)
        self.ui.mark_input1_button.clicked.connect(self.mark_input1_button)
        self.ui.mark_input2_button.clicked.connect(self.mark_input2_button)
        self.ui.mark_output_button.clicked.connect(self.mark_output_button)
        self.ui.mark_working_button.clicked.connect(self.mark_working_button)
        self.ui.calibrate_button.clicked.connect(self.toggle_calibrate_button)
        self.ui.clear_mark_button.clicked.connect(self.clear_mark_button)
        self.ui.clear_track_button.clicked.connect(self.clear_track_button)
        self.ui.start_button.clicked.connect(self.start_timer_button)

        # set mouse event function
        self.ui.display_camera_frame.mousePressEvent = self.camera_frame_mouse_event

        # set status of button and frame
        self.ui.mark_input1_button.setEnabled(False)
        self.ui.mark_input2_button.setEnabled(False)
        self.ui.mark_output_button.setEnabled(False)
        self.ui.mark_working_button.setEnabled(False)
        self.ui.start_button.setEnabled(False)

        # set stylesheet for text
        self.ui.text_input1_on_camera.setStyleSheet('background: transparent;color: rgb(255, 0, 0);')
        self.ui.text_input2_on_camera.setStyleSheet('background: transparent;color: rgb(255, 150, 0);')
        self.ui.text_output_on_camera.setStyleSheet('background: transparent;color: rgb(255, 80, 0);')
        self.ui.text_work_on_camera.setStyleSheet('background: transparent;color: rgb(255, 80, 150);')
        self.ui.text_calibrate_input1_on_camera.setStyleSheet('background: transparent;color: rgb(255, 0, 0);')
        self.ui.text_calibrate_input2_on_camera.setStyleSheet('background: transparent;color: rgb(255, 150, 0);')
        self.ui.text_calibrate_output_on_camera.setStyleSheet('background: transparent;color: rgb(255, 80, 0);')
        self.ui.text_calibrate_work_on_camera.setStyleSheet('background: transparent;color: rgb(255, 80, 150);')
        self.ui.text_input1_on_camera.setVisible(False)
        self.ui.text_input2_on_camera.setVisible(False)
        self.ui.text_output_on_camera.setVisible(False)
        self.ui.text_work_on_camera.setVisible(False)
        self.ui.text_calibrate_input1_on_camera.setVisible(False)
        self.ui.text_calibrate_input2_on_camera.setVisible(False)
        self.ui.text_calibrate_output_on_camera.setVisible(False)
        self.ui.text_calibrate_work_on_camera.setVisible(False)

        # set text value for dial
        self.ui.text_dial_camera_number.setText(str(self.ui.dial_camera_number.value()))
        self.ui.text_dial_detect_area.setText(str(self.ui.dial_detect_area.value()))
        self.ui.text_dial_hsv_range.setText(str(self.ui.dial_hsv_range.value()))
        self.ui.text_dial_calibrate_input1.setText(str(self.ui.dial_calibrate_input1.value()))
        self.ui.text_dial_calibrate_input2.setText(str(self.ui.dial_calibrate_input2.value()))
        self.ui.text_dial_calibrate_output.setText(str(self.ui.dial_calibrate_output.value()))
        self.ui.text_dial_calibrate_work.setText(str(self.ui.dial_calibrate_work.value()))
        self.ui.text_dial_center_point_boundary.setText(str(self.ui.dial_center_point_boundary.value()))

    def toggle_calibrate_button(self):
        if self.is_calibrate:
            self.ui.text_calibrate.setText('Calibrate is off')
            self.ui.text_calibrate.setStyleSheet('color:red')
            self.is_calibrate = False
            self.calibrate.set_calibrate_area_status(False)
        else:
            self.ui.text_calibrate.setText('Calibrate is on')
            self.ui.text_calibrate.setStyleSheet('color:lime')
            self.is_calibrate = True
            self.calibrate.set_calibrate_area_status(True)

    def toggle_display_mark_area(self):
        if self.toggle_mark_area_status:
            self.ui.text_mark_area.setText('Mark is off')
            self.ui.text_mark_area.setStyleSheet('color:red')
            # self.ui.display_mark_area_frame.setVisible(False)
            self.ui.mark_input1_button.setEnabled(False)
            self.ui.mark_input2_button.setEnabled(False)
            self.ui.mark_output_button.setEnabled(False)
            self.ui.mark_working_button.setEnabled(False)
            self.toggle_mark_area_status = False
        else:
            self.ui.text_mark_area.setText('Mark is on')
            self.ui.text_mark_area.setStyleSheet('color:lime')
            self.ui.mark_input1_button.setEnabled(True)
            self.ui.mark_input2_button.setEnabled(True)
            self.ui.mark_output_button.setEnabled(True)
            self.ui.mark_working_button.setEnabled(True)
            self.toggle_mark_area_status = True

    def get_toggle_mark_status(self):
        return self.toggle_mark_area_status

    def clear_mark_button(self):
        self.image_storage.reset_background_image_for_mark()
        # reset all position
        self.calibrate.set_input1_position((-1, -1))
        self.calibrate.set_input2_position((-1, -1))
        self.calibrate.set_output_position((-1, -1))
        self.calibrate.set_work_position((-1, -1))

        # enable all mark button
        self.ui.mark_input1_button.setEnabled(True)
        self.ui.mark_input2_button.setEnabled(True)
        self.ui.mark_output_button.setEnabled(True)
        self.ui.mark_working_button.setEnabled(True)
        print('clear mark button clicked')

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

    def mark_input1_button(self):
        self.which_marked_area = 0
        self.ui.mark_input1_button.setEnabled(False)
        self.ui.text_input1_on_camera.setVisible(True)
        self.ui.text_calibrate_input1_on_camera.setVisible(True)
        text = str('0') + str('/') + str(self.ui.dial_calibrate_input1.value())
        self.ui.text_calibrate_input1_on_camera.setText(text)

    def mark_input2_button(self):
        self.which_marked_area = 1
        self.ui.mark_input2_button.setEnabled(False)
        self.ui.text_input2_on_camera.setVisible(True)
        self.ui.text_calibrate_input2_on_camera.setVisible(True)
        text = str('0') + str('/') + str(self.ui.dial_calibrate_input2.value())
        self.ui.text_calibrate_input2_on_camera.setText(text)

    def mark_output_button(self):
        self.which_marked_area = 2
        self.ui.mark_output_button.setEnabled(False)
        self.ui.text_output_on_camera.setVisible(True)
        self.ui.text_calibrate_output_on_camera.setVisible(True)
        text = str('0') + str('/') + str(self.ui.dial_calibrate_output.value())
        self.ui.text_calibrate_output_on_camera.setText(text)

    def mark_working_button(self):
        self.which_marked_area = 3
        self.ui.mark_working_button.setEnabled(False)
        self.ui.text_work_on_camera.setVisible(True)
        self.ui.text_calibrate_work_on_camera.setVisible(True)
        text = str('0') + str('/') + str(self.ui.dial_calibrate_work.value())
        self.ui.text_calibrate_work_on_camera.setText(text)

    # Set which type of image (RGB,HSV,GRAYSCALE)
    def set_show_image_type(self, new_type):
        self.show_image_type = new_type

    def get_show_image_type(self):
        return self.show_image_type

    # Exit program Button
    def exit_button(self):
        print('Exit Button Clicked...')
        sys.exit(0)

    # Go to setting page from main page button
    def go_to_setting_button(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    # Back to main page from setting page button
    def go_to_main_button(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    # Toggle display detect area Button
    def toggle_display_detect_button(self):
        if self.toggle_detect_status:
            self.ui.text_detect.setText('Detection is off')
            self.ui.text_detect.setStyleSheet('color:red')
            self.toggle_detect_status = False
        else:
            self.ui.text_detect.setText('Detection is on')
            self.ui.text_detect.setStyleSheet('color:lime')
            self.toggle_detect_status = True

    def get_toggle_detect_status(self):
        return self.toggle_detect_status

    # Toggle display track area Button
    def toggle_display_track_button(self):
        if self.toggle_track_status:
            self.ui.text_track.setText('Tracking is off')
            self.ui.text_track.setStyleSheet('color:red')
            self.toggle_track_status = False
        else:
            self.ui.text_track.setText('Tracking is on')
            self.ui.text_track.setStyleSheet('color:lime')
            self.toggle_track_status = True

    def get_toggle_track_status(self):
        return self.toggle_track_status

    def clear_track_button(self):
        self.image_storage.reset_background_image_for_track()
        print('clear track button clicked')

    # Open Camera Button
    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        # setup displayed text and button when camera open
        self.ui.text_image_type.setText('RGB Mode')
        self.ui.text_image_type.setStyleSheet('color:gold')
        self.ui.text_track.setText('Tracking is on')
        self.ui.text_track.setStyleSheet('color:lime')
        self.ui.text_mark_area.setText('Mark is on')
        self.ui.text_mark_area.setStyleSheet('color:lime')
        self.ui.text_detect.setText('Detection is on')
        self.ui.text_detect.setStyleSheet('color:lime')
        self.ui.text_calibrate.setText('calibrate is on')
        self.ui.text_calibrate.setStyleSheet('color:lime')
        self.toggle_calibrate_status = True
        self.toggle_detect_status = True
        self.toggle_track_status = True
        self.toggle_mark_area_status = True
        self.is_calibrate = True
        # self.ui.display_mark_area_frame.setVisible(True)
        self.ui.mark_input1_button.setEnabled(True)
        self.ui.mark_input2_button.setEnabled(True)
        self.ui.mark_output_button.setEnabled(True)
        self.ui.mark_working_button.setEnabled(True)

        # Create Thread for input_video
        self.thread_input_video = GuiInputVideo(self, self.image_storage)
        self.thread_input_video.start()

        # Create Thread for output_video
        self.thread_output_video = GuiProcessOutput(self, self.image_storage)
        self.thread_output_video.start()

        # Disable button
        self.ui.open_camera_button.setEnabled(False)

    # Receive image from other class and display to gui
    def display_image_to_camera_zone(self, receive_image):
        time.sleep(0.025)
        self.ui.display_camera_frame.setPixmap(QPixmap.fromImage(receive_image))

    # Get x,y from mouse clicked method
    def camera_frame_mouse_event(self, event):
        x = event.pos().x()
        y = event.pos().y()
        # check which select color button is pressed
        # select left color button is pressed
        if self.left_or_right_color == 0:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                # first click will be start thread once
                if self.is_first_left_click:
                    self.left_color_detection = GuiColorDetection(self, self.image_storage)
                    self.left_color_detection.start()
                    self.left_color_detection.set_position(x, y)
                    self.left_color_detection.set_hsv()
                    self.left_color_detection.set_color(self.image_storage.get_input_image()[y, x])
                    self.is_first_left_click = False
                    # disable clear mark button
                    self.ui.clear_mark_button.setEnabled(False)

                # set new color without start thread
                else:
                    self.left_color_detection.set_position(x, y)
                    self.left_color_detection.set_hsv()
                    self.left_color_detection.set_color(self.image_storage.get_input_image()[y, x])

        # select right color button is pressed
        elif self.left_or_right_color == 1:
            # check which mouse button is clicked
            if event.buttons() == QtCore.Qt.LeftButton:
                # first click will be start thread once
                if self.is_first_right_click:
                    self.right_color_detection = GuiColorDetection(self, self.image_storage)
                    self.right_color_detection.start()
                    self.right_color_detection.set_position(x, y)
                    self.right_color_detection.set_hsv()
                    self.right_color_detection.set_color(self.image_storage.get_input_image()[y, x])
                    self.is_first_right_click = False
                    # disable clear mark button
                    self.ui.clear_mark_button.setEnabled(False)
                # set new color without start thread
                else:
                    self.right_color_detection.set_position(x, y)
                    self.right_color_detection.set_hsv()
                    self.right_color_detection.set_color(self.image_storage.get_input_image()[y, x])

        # set state to -1 to not allow select color without select color button
        self.left_or_right_color = -1

        # create temp variable to load image due to long command
        background_image = self.image_storage.get_background_image_for_mark()
        if self.which_marked_area == 0:
            cv2.putText(background_image, 'Input1', (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 0, 255))
            cv2.circle(background_image, (x, y), 2, (0, 0, 255), 6)
            self.calibrate.set_input1_position((x, y))
            # disable click from input1
            self.which_marked_area = -1

        elif self.which_marked_area == 1:
            cv2.putText(background_image, 'Input2', (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 150, 255))
            cv2.circle(background_image, (x, y), 2, (0, 150, 255), 6)
            self.calibrate.set_input2_position((x, y))
            # disable click from input1
            self.which_marked_area = -1

        elif self.which_marked_area == 2:
            cv2.putText(background_image, 'Output', (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 80, 255))
            cv2.circle(background_image, (x, y), 2, (0, 80, 255), 6)
            self.calibrate.set_output_position((x, y))
            # disable click from input1
            self.which_marked_area = -1

        elif self.which_marked_area == 3:
            cv2.putText(background_image, 'Work', (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (150, 80, 255))
            cv2.circle(background_image, (x, y), 2, (150, 80, 255), 6)
            self.calibrate.set_work_position((x, y))
            # disable click from input1
            self.which_marked_area = -1

    def display_calibrated_number_input1(self, number):
        text = str(number) + str('/') + str(self.ui.dial_calibrate_input1.value())
        self.ui.text_calibrate_input1_on_camera.setText(text)

    def display_calibrated_number_input2(self, number):
        text = str(number) + str('/') + str(self.ui.dial_calibrate_input2.value())
        self.ui.text_calibrate_input2_on_camera.setText(text)

    def display_calibrated_number_output(self, number):
        text = str(number) + str('/') + str(self.ui.dial_calibrate_output.value())
        self.ui.text_calibrate_output_on_camera.setText(text)

    def display_calibrated_number_work(self, number):
        text = str(number) + str('/') + str(self.ui.dial_calibrate_work.value())
        self.ui.text_calibrate_work_on_camera.setText(text)

    def get_reference_calibrate(self):
        return self.calibrate

    def get_reference_layout(self):
        return self.ui

    def start_timer_button(self):
        self.timer = GuiTimer(self)
        self.timer.start()

