import threading

import cv2
from threading import Thread

class GuiInputVideo(Thread):
    def __init__(self):
        super().__init__()
        self.camera_number = 0
        self.webcam = cv2.VideoCapture(self.camera_number)
        self.input_image = None
        self.camera_status = False

    def get_image_from_camera(self):
        print('Start receive image ...')
        while(self.camera_status):
            ret,input_image = self.webcam.read()
            if ret:
                self.input_image = input_image
        print('Stop receive image ...')
        self.webcam.release()

    def get_input_image(self):
        return self.input_image

    def set_camera_status(self,status):
        self.camera_status = status

    def get_camera_status(self):
        return self.camera_status

    def set_camera_number(self,number):
        self.camera_number = number

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.get_image_from_camera()