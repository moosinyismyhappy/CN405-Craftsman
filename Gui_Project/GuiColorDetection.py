import threading
import cv2
import numpy as np
from Gui_Project.GuiTracking import GuiTracking
from threading import Thread


class GuiColorDetection(Thread):
    def __init__(self, gui, input_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = input_storage
        self.value_for_calibrate = self.gui.get_reference_value_for_calibrate()
        self.layout = self.gui.get_reference_layout()
        self.tracking = GuiTracking(self.gui, self.image_storage, self)
        self.x_position = -1
        self.y_position = -1
        self.w = -1
        self.h = -1
        self.x = -1
        self.y = -1
        self.hsv_list = None
        self.hsv_lower = None
        self.hsv_upper = None
        self.is_first_detect = True
        self.bgr = [-1, -1, -1]
        self.side_status = -1

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.detect_color()

    def set_side_status(self, status):
        self.side_status = status

    def set_color(self, bgr):
        self.bgr = bgr

    def get_color(self):
        b = int(self.bgr[0] + 50)
        g = int(self.bgr[1] + 50)
        r = int(self.bgr[2] + 50)
        return b, g, r

    def set_hsv(self):
        temp_x = self.get_position()[0]
        temp_y = self.get_position()[1]

        # set get hsv to process lower and upper
        self.hsv_list = list(self.image_storage.get_hsv_image_for_detection()[temp_y, temp_x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def __hsv_upper_process(self):
        hsv_range = self.layout.dial_hsv_range.value() / 100
        h_upper = int(self.hsv_list[0] * (1 + hsv_range))
        s_upper = int(self.hsv_list[1] * (1 + hsv_range))
        v_upper = int(self.hsv_list[2] * (1 + hsv_range))

        # Set limit maximum of hsv value not more than 255
        if h_upper >= 255: h_upper = 255
        if s_upper >= 255: s_upper = 255
        if v_upper >= 255: v_upper = 255

        # combine hsv separate value to list
        self.hsv_upper = [h_upper, s_upper, v_upper]

    def __hsv_lower_process(self):
        hsv_range = self.layout.dial_hsv_range.value() / 100

        h_lower = int(self.hsv_list[0] * (1 - hsv_range))
        s_lower = int(self.hsv_list[1] * (1 - hsv_range))
        v_lower = int(self.hsv_list[2] * (1 - hsv_range))

        # Set limit minimum of hsv value not more than 255
        if h_lower >= 255: h_lower = 255
        if s_lower >= 255: s_lower = 255
        if v_lower >= 255: v_lower = 255

        # combine hsv separate value to list
        self.hsv_lower = [h_lower, s_lower, v_lower]

    def set_position(self, x, y):
        self.x_position = x
        self.y_position = y

    def get_position(self):
        return self.x_position, self.y_position

    def print_hsv_value(self):
        print(self.hsv_list, self.hsv_lower, self.hsv_upper)

    def detect_color(self):
        print('Starting Detect color ...')
        while True:
            try:
                color_lower = np.array([self.hsv_lower[0], self.hsv_lower[1], self.hsv_lower[2]])
                color_upper = np.array([self.hsv_upper[0], self.hsv_upper[1], self.hsv_upper[2]])
                color_mask = cv2.inRange(self.image_storage.get_hsv_image_for_detection(), color_lower, color_upper)
            except:
                print('Exception from detect_color class ColorDetection')
                continue

            kernal = np.ones((5, 5), "int8")
            color_mask = cv2.dilate(color_mask, kernal)
            contours, hierarchy = cv2.findContours(color_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                # get detect area from dial setting
                if area > self.layout.dial_detect_area.value():
                    self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
                    center_position = int((2 * self.x + self.w) / 2), int((2 * self.y + self.h) / 2)
                    if self.is_first_detect:
                        center_point_boundary = [self.x, self.y, self.x + self.w, self.y + self.h]
                        self.tracking.set_center_point_boundary(center_point_boundary)
                        self.tracking.set_current_position(center_point_boundary)
                        self.tracking.set_previous_position(center_point_boundary)
                        self.tracking.set_current_direction(-1)
                        self.tracking.set_previous_direction(-1)
                        self.is_first_detect = False
                    else:
                        self.tracking.is_center_point_in_boundary(center_position)
                        if self.tracking.get_is_position_out_of_boundary():
                            center_point_boundary = [self.x, self.y, self.x + self.w, self.y + self.h]
                            self.tracking.set_center_point_boundary(center_point_boundary)

                            # when timer is ready check center position is in any created area
                            if self.value_for_calibrate.get_timer_ready_status():
                                input1_status = self.tracking.is_in_input1_area(center_position)
                                input2_status = self.tracking.is_in_input2_area(center_position)
                                output_status = self.tracking.is_in_output_area(center_position)
                                work_status = self.tracking.is_in_work_area(center_position)

                                self.value_for_calibrate.set_input1_area_counter(input1_status)
                                self.value_for_calibrate.set_input2_area_counter(input2_status)
                                self.value_for_calibrate.set_output_area_counter(output_status)
                                self.value_for_calibrate.set_work_area_counter(work_status)

                                # clear rectangle list
                                self.value_for_calibrate.get_rectangle_list().clear()

                                # disable text on camera
                                self.layout.text_input1_on_camera.setVisible(False)
                                self.layout.text_input2_on_camera.setVisible(False)
                                self.layout.text_output_on_camera.setVisible(False)
                                self.layout.text_work_on_camera.setVisible(False)
                                self.layout.text_calibrate_input1_on_camera.setVisible(False)
                                self.layout.text_calibrate_input2_on_camera.setVisible(False)
                                self.layout.text_calibrate_output_on_camera.setVisible(False)
                                self.layout.text_calibrate_work_on_camera.setVisible(False)

                                # disable display track and mark
                                self.gui.toggle_track_status = False
                                self.gui.toggle_mark_area_status = False

                                # enable text time
                                self.layout.text_input1_time.setVisible(True)
                                self.layout.text_input2_time.setVisible(True)
                                self.layout.text_output_time.setVisible(True)
                                self.layout.text_work_time.setVisible(True)
                                self.layout.text_cycle_time.setVisible(True)
                                self.layout.text_display_input1_time.setVisible(True)
                                self.layout.text_display_input2_time.setVisible(True)
                                self.layout.text_display_output_time.setVisible(True)
                                self.layout.text_display_work_time.setVisible(True)
                                self.layout.text_display_cycle_time.setVisible(True)

                                # left hand
                                if self.side_status == 0:
                                    # find where area that center at
                                    self.tracking.where_is_center_in_area_left(center_position)

                                # right hand
                                elif self.side_status == 1:
                                    # find where area that center at
                                    self.tracking.where_is_center_in_area_right(center_position)

                    # check detect button is active
                    if self.gui.get_toggle_detect_status():
                        # Draw rectangle over detect color
                        cv2.rectangle(self.image_storage.get_input_image(), (self.x, self.y),
                                      (self.x + self.w, self.y + self.h), (self.get_color()), 2)

                        # Draw center point on detect rectangle
                        cv2.circle(self.image_storage.get_input_image(), center_position, 2, (self.get_color()), 2)

                        # Draw rectangle boundary over detect
                        # x1 = self.tracking.get_center_point_boundary()[0]
                        # y1 = self.tracking.get_center_point_boundary()[1]
                        # x2 = self.tracking.get_center_point_boundary()[2]
                        # y2 = self.tracking.get_center_point_boundary()[3]
                        # cv2.rectangle(self.image_storage.get_input_image(), (x1, y1), (x2, y2), (150, 150, 150), 2)

            # draw calibrated area
            image_frame = self.image_storage.get_input_image()
            if self.value_for_calibrate.get_display_input1_area_status():
                x1 = self.value_for_calibrate.get_input1_calibrate_area()[0]
                y1 = self.value_for_calibrate.get_input1_calibrate_area()[1]
                x2 = self.value_for_calibrate.get_input1_calibrate_area()[2]
                y2 = self.value_for_calibrate.get_input1_calibrate_area()[3]
                cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            if self.value_for_calibrate.get_display_input2_area_status():
                x1 = self.value_for_calibrate.get_input2_calibrate_area()[0]
                y1 = self.value_for_calibrate.get_input2_calibrate_area()[1]
                x2 = self.value_for_calibrate.get_input2_calibrate_area()[2]
                y2 = self.value_for_calibrate.get_input2_calibrate_area()[3]
                cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)

            if self.value_for_calibrate.get_display_output_area_status():
                x1 = self.value_for_calibrate.get_output_calibrate_area()[0]
                y1 = self.value_for_calibrate.get_output_calibrate_area()[1]
                x2 = self.value_for_calibrate.get_output_calibrate_area()[2]
                y2 = self.value_for_calibrate.get_output_calibrate_area()[3]
                cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 80, 255), 2)

            if self.value_for_calibrate.get_display_work_area_status():
                x1 = self.value_for_calibrate.get_work_calibrate_area()[0]
                y1 = self.value_for_calibrate.get_work_calibrate_area()[1]
                x2 = self.value_for_calibrate.get_work_calibrate_area()[2]
                y2 = self.value_for_calibrate.get_work_calibrate_area()[3]
                cv2.rectangle(image_frame, (x1, y1), (x2, y2), (150, 80, 255), 2)