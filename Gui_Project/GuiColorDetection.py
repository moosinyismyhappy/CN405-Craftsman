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
        self.tracking = GuiTracking(self.gui, self.image_storage,self)
        self.x_position = -1
        self.y_position = -1
        self.w = -1
        self.h = -1
        self.x = -1
        self.y = -1
        self.hsv_range = 0.2
        self.hsv_list = None
        self.hsv_lower = None
        self.hsv_upper = None
        self.is_first_detect = True
        self.bgr = [-1,-1,-1]

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.detect_color()

    def set_color(self,bgr):
        self.bgr = bgr

    def get_color(self):
        return self.bgr

    def set_hsv(self):
        temp_x = self.get_position()[0]
        temp_y = self.get_position()[1]

        # set get hsv to process lower and upper
        self.hsv_list = list(self.image_storage.get_hsv_image_for_detection()[temp_y, temp_x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def __hsv_upper_process(self):
        h_upper = int(self.hsv_list[0] * (1 + self.hsv_range))
        s_upper = int(self.hsv_list[1] * (1 + self.hsv_range))
        v_upper = int(self.hsv_list[2] * (1 + self.hsv_range))

        # Set limit maximum of hsv value not more than 255
        if h_upper >= 255: h_upper = 255
        if s_upper >= 255: s_upper = 255
        if v_upper >= 255: v_upper = 255

        # combine hsv separate value to list
        self.hsv_upper = [h_upper, s_upper, v_upper]

    def __hsv_lower_process(self):
        h_lower = int(self.hsv_list[0] * (1 - self.hsv_range))
        s_lower = int(self.hsv_list[1] * (1 - self.hsv_range))
        v_lower = int(self.hsv_list[2] * (1 - self.hsv_range))

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
                if area > 3000:
                    self.x, self.y, self.w, self.h = cv2.boundingRect(contour)
                    center_position = int((2 * self.x + self.w) / 2), int((2 * self.y + self.h) / 2)
                    if self.is_first_detect:
                        center_boundary = [self.x, self.y, self.x + self.w, self.y + self.h]
                        self.tracking.set_center_boundary(center_boundary)
                        self.tracking.set_current_position(center_position)
                        self.tracking.set_previous_position(center_position)
                        self.tracking.set_current_direction(-1)
                        self.tracking.set_previous_direction(-1)
                        self.is_first_detect = False
                    else:
                        self.tracking.is_center_in_boundary(center_position)
                        if self.tracking.get_is_position_out_of_boundary():
                            center_boundary = [self.x, self.y, self.x + self.w, self.y + self.h]
                            self.tracking.set_center_boundary(center_boundary)

                    # check detect button is active
                    if self.gui.get_toggle_detect_status():
                        # Draw rectangle over detect color
                        cv2.rectangle(self.image_storage.get_input_image(), (self.x, self.y),
                                          (self.x + self.w, self.y + self.h), (0, 255, 0), 2)

                        # Draw center point on detect rectangle
                        cv2.circle(self.image_storage.get_input_image(), center_position, 2, (0, 0, 255), 2)

                        # Draw rectangle boundary over detect
                        cv2.rectangle(self.image_storage.get_input_image(), (
                            self.tracking.get_center_boundary()[0], self.tracking.get_center_boundary()[1]),
                                      (self.tracking.get_center_boundary()[2], self.tracking.get_center_boundary()[3]),
                                      (0, 255, 255), 2)
