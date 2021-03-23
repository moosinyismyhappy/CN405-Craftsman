import cv2
import threading
import numpy as np
from threading import Thread
from InputVideo import *


class ColorDetection(Thread):

    def __init__(self, input_storage):
        super().__init__()
        self.image_storage = input_storage
        self.bg = cv2.imread('../resources/images/black_background.png')
        self.x_cord = None
        self.y_cord  = None
        self.is_first_track = True
        self.hsv_image = None
        self.hsv_list = None
        self.hsv_lower = None
        self.hsv_upper = None
        self.hsv_range = 0.15
        self.w = -1
        self.h = -1
        self.x = -1
        self.y = -1
        self.prev = None
        self.curr = None
        self.prev_status = None
        self.curr_status = None
        self.count = 0

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

    def set_x_y(self,x,y):
        self.x_cord = x
        self.y_cord = y

    def get_x_y(self):
        return self.x_cord,self.y_cord

    def set_hsv(self):
        temp_x = self.get_x_y()[0]
        temp_y = self.get_x_y()[1]
        self.hsv_list = list(self.image_storage.get_hsv_image()[temp_y,temp_x])
        self.__hsv_lower_process()
        self.__hsv_upper_process()

    def print_hsv(self):
        print('HSV:', self.hsv_list, 'HSV-Lower:', self.hsv_lower, 'HSV-Upper:', self.hsv_upper)

    def detect_color(self):
        print('Detecting color ...')
        while True:

            cv2.imshow('test',self.bg)
            cv2.waitKey(1)

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
                    cv2.rectangle(temp, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)

                    # Calculate center coordinates
                    center = int((2 * self.x + self.w) / 2), int((2 * self.y + self.h) / 2)

                    # Tracking
                    self.tracking_detection(temp,center)
                    self.is_first_track = False
                    self.count += 1

                    # Draw Circle over temp image
                    #cv2.circle(temp, center, 2, (255, 255, 0), 2)

                    # add detected image to image storage
                    self.image_storage.add_detected_image(temp)

    def tracking_detection(self,input_image,input_cord):

        if not self.is_first_track:

            if self.count%2 == 0:
                self.prev = self.curr
                self.curr = input_cord
                self.prev_status = self.curr_status

                diff_x = self.curr[0] - self.prev[0]
                diff_y = self.curr[1] - self.prev[1]
                #print(self.curr,self.prev,diff_x,diff_y,self.count)

                if diff_x and diff_y > 0:
                    self.curr_status = (1,1)
                elif diff_x and diff_y < 0:
                    self.curr_status = (-1,-1)
                elif diff_x > 0 and diff_y < 0:
                    self.curr_status = (1,-1)
                elif diff_x < 0 and diff_y > 0:
                    self.curr_status = (-1,1)

                if self.prev_status != self.curr_status:
                    print('Change Direction from',self.prev_status,self.prev,'to',self.curr_status,self.curr,'with diff',diff_x,diff_y)
                    cv2.circle(self.bg, input_cord , 2, (255, 255, 0), 2)

                # Restart counter
                self.count = 0

        else:
            self.prev = input_cord
            self.curr = input_cord
            self.curr_status = (0,0)

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.detect_color()
