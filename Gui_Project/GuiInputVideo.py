import threading
import time
from threading import Thread
import cv2

class GuiInputVideo(Thread):

    def __init__(self,gui,image_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = image_storage
        self.camera_number = self.gui.ui.dial_camera_number.value()
        #self.webcam = cv2.VideoCapture(self.camera_number)
        self.webcam = cv2.VideoCapture('../resources/videos/Full_Working1.mp4')

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.__get_image_from_camera()

    def set_camera_number(self,number):
        self.camera_number = number

    def __get_image_from_camera(self):
        print('Start receive image ...')
        while True:
            ret,input_image = self.webcam.read()
            if ret:
                time.sleep(0.02)
                input_image = cv2.resize(input_image,(640,480))
                self.image_storage.set_input_image(input_image)
            else:
                break
        print('Stop receive image ...')
        self.webcam.release()



