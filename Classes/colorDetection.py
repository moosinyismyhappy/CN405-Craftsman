import cv2
import threading
import numpy as np
from threading import Thread
from inputVideo import *


class colorDetection(Thread):

    def __init__(self):
        super().__init__()
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

        if h_upper >= 255: h_upper = 255
        if s_upper >= 255: s_upper = 255
        if v_upper >= 255: v_upper = 255

        self.hsv_upper = [h_upper, s_upper, v_upper]

    def __hsv_lower_process(self):

        h_lower = int(self.hsv_list[0] * (1 - self.hsv_range))
        s_lower = int(self.hsv_list[1] * (1 - self.hsv_range))
        v_lower = int(self.hsv_list[2] * (1 - self.hsv_range))

        if h_lower >= 255: h_lower = 255
        if s_lower >= 255: s_lower = 255
        if v_lower >= 255: v_lower = 255

        self.hsv_lower = [h_lower, s_lower, v_lower]

    def set_hsv(self, input_hsv_image, x, y):
        self.hsv_image = input_hsv_image
        self.hsv_list = list(input_hsv_image[y, x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def print_hsv(self):
        print('HSV:', self.hsv_list, 'HSV-Lower:', self.hsv_lower, 'HSV-Upper:', self.hsv_upper)

    def set_detected_area(self,xVal,yVal,wVal,hVal):
        self.x = xVal
        self.y = yVal
        self.w = wVal
        self.h = hVal

    def get_detected_area(self):
        return [self.x,self.y,self.w,self.h]

    def detect_color(self):
        print('Detecting color ...')




