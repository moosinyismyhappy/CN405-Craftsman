import cv2
import threading
from threading import Thread
from ColorDetection import *


class MouseDetection(Thread):

    def __init__(self, input_storage):
        super().__init__()
        self.image_storage = input_storage
        self.left_first_click = True
        self.right_first_click = True

        # Thread-3 color detection for Left Hand , Thread-4 color detection for Right Hand
        self.color_left_hand = None
        self.color_right_hand = None

    def is_left_first_click(self):
        return self.left_first_click

    def is_right_first_click(self):
        return self.right_first_click

    def __mouse_detection_process(self, event, x, y, flags, param):
        if event is cv2.EVENT_LBUTTONDOWN:
            if not self.is_left_first_click():
                self.color_left_hand.set_x_y(x, y)
                self.color_left_hand.set_hsv()
            else:
                print('Starting color detection - Left Hand ...')
                self.color_left_hand = ColorDetection(self.image_storage)
                self.color_left_hand.set_x_y(x, y)
                self.color_left_hand.set_hsv()
                self.color_left_hand.start()
                self.left_first_click = False

        elif event is cv2.EVENT_RBUTTONDOWN:
            if not self.is_right_first_click():
                self.color_right_hand.set_x_y(x,y)
                self.color_right_hand.set_hsv()
            else:
                print('Starting color detection - right Hand ...')
                self.color_right_hand = ColorDetection(self.image_storage)
                self.color_right_hand.set_x_y(x, y)
                self.color_right_hand.set_hsv()
                self.color_right_hand.start()
                self.right_first_click = False

    def start_mouse_detection(self, winNameVal):
        cv2.setMouseCallback(winNameVal, self.__mouse_detection_process)
