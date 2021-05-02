import threading
from threading import Thread

import cv2
import numpy as np

from Gui_Project.GuiTracking import GuiTracking


class GuiColorDetection(Thread):

    def __init__(self, gui, input_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = input_storage
        self.tracking = None
        self.tracking_status = 0
        self.center_pos = (-1,-1)
        self.x_pos = -1
        self.y_pos = -1
        self.w = -1
        self.h = -1
        self.x = -1
        self.y = -1
        self.hsv_range = 0.2
        self.hsv_list = None
        self.hsv_lower = None
        self.hsv_upper = None

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        # time.sleep(0.1)
        self.detect_color()

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

    def set_hsv(self):
        temp_x = self.get_pos()[0]
        temp_y = self.get_pos()[1]
        self.hsv_list = list(self.image_storage.get_hsv_image_for_detect()[temp_y, temp_x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def detect_color(self):
        print('Starting Detect color ...')
        while self.image_storage.get_storage_status():
            try:
                color_lower = np.array([self.hsv_lower[0], self.hsv_lower[1], self.hsv_lower[2]])
                color_upper = np.array([self.hsv_upper[0], self.hsv_upper[1], self.hsv_upper[2]])
                color_mask = cv2.inRange(self.image_storage.get_hsv_image_for_detect(), color_lower, color_upper)
            except:
                print('Exception from detect_color Class ColorDetection')
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

                    self.center_pos = int((2 * self.x + self.w) / 2), int((2 * self.y + self.h) / 2)

                    # First detection -> Set value for first tracking
                    if self.tracking_status == 0:
                        print('First Tracking')
                        self.tracking = GuiTracking(self.gui,self.image_storage)
                        self.tracking.set_center_position(self.center_pos)
                        self.tracking_status = 1

                    # After first detection -> Set value for tracking
                    elif self.tracking_status ==1:
                        print('After first tracking')
                        self.tracking.set_center_position(self.center_pos)
                        self.tracking.print_center()

                    elif self.tracking_status ==2:
                        print('temp')


                    detected_image = cv2.rectangle(self.image_storage.get_input_image(), (self.x, self.y),
                                                   (self.x + self.w, self.y + self.h), (0, 255, 0), 2)

                    self.image_storage.set_detected_image(detected_image)

    def print_hsv_value(self):
        print(self.hsv_list, self.hsv_lower, self.hsv_upper)

    def set_pos(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def get_pos(self):
        return self.x_pos, self.y_pos
