import cv2
import threading
import numpy as np
from threading import Thread
from InputVideo import *


class ColorDetection(Thread):

    def __init__(self,input_storage):
        super().__init__()
        self.image_storage = input_storage
        self.hsv_image = None
        self.hsv_list = None
        self.hsv_lower = None
        self.hsv_upper = None
        self.hsv_range = 0.15
        self.w = -1
        self.h = -1
        self.x = -1
        self.y = -1

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

    def set_hsv(self, x, y):
        self.hsv_list = list(self.image_storage.get_hsv_image()[y,x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def print_hsv(self):
        print('HSV:', self.hsv_list, 'HSV-Lower:', self.hsv_lower, 'HSV-Upper:', self.hsv_upper)

    def detect_color(self):
        print('Detecting color ...')
        while True:
            try:
                color_lower = np.array([self.hsv_lower[0], self.hsv_lower[1], self.hsv_lower[2]])
                color_upper = np.array([self.hsv_upper[0], self.hsv_upper[1], self.hsv_upper[2]])
                color_mask = cv2.inRange(self.image_storage.get_hsv_image(), color_lower, color_upper)
            except:
                print('Exception from detect_color Class ColorDetection')
                continue

            kernal = np.ones((5, 5), "uint8")
            color_mask = cv2.dilate(color_mask, kernal)
            contours, hierarchy = cv2.findContours(color_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 3000:
                    self.x, self.y, self.w, self.h = cv2.boundingRect(contour)

                    # Create temp to copy original images
                    temp = self.image_storage.get_image().copy()

                    # Draw Rectangle over temp image
                    cv2.rectangle(temp, (self.x,self.y), (self.x + self.w, self.y+self.h), (0,255,0), 2)

                    # add detected image to image storage
                    self.image_storage.add_detected_image(temp)

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.detect_color()
