import cv2
import threading
from threading import Thread
from colorDetection import *


class mouseDetection(Thread):

    def __init__(self):
        super().__init__()
        self.hsv_image = None
        self.left_first_click = True
        self.right_first_click = True
        # Thread-3 for Left Hand
        self.left_hand = None
        # Thread-4 for Right Hand
        self.right_hand = None

    def is_left_first_click(self):
        return self.left_first_click

    def is_right_first_click(self):
        return self.right_first_click

    def __mouse_detection_process(self, event, x, y, flags, param):

        if event is cv2.EVENT_LBUTTONDOWN:

            if not self.is_left_first_click():
                self.left_hand.set_hsv(self.hsv_image,x,y)
                self.left_hand.detect_color()
                print(self.left_hand.get_detected_area())
                self.left_hand.print_hsv()

            else:
                print('Starting color detection - Left Hand ...')
                # create colorDetection for Left Hand
                self.left_hand = colorDetection()
                self.left_hand.set_hsv(self.hsv_image,x,y)
                self.left_hand.print_hsv()
                self.left_first_click = False

        """elif event is cv2.EVENT_RBUTTONDOWN:

            if not self.is_right_first_click():
                print('do color detection')

            else:
                print('Starting color detection - Right Hand ...')
                # create colorDetection for Right Hand
                self.right_hand = colorDetection(list(self.hsv_image[y,x]))
                self.right_first_click = False"""

    def start_mouse_detection(self, winNameVal, hsvImage):
        self.hsv_image = hsvImage
        cv2.setMouseCallback(winNameVal, self.__mouse_detection_process)
