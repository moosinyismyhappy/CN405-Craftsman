import threading
from threading import Thread
import cv2

class GuiInputVideo(Thread):

    def __init__(self,image_storage):
        super().__init__()
        self.image_storage = image_storage
        self.camera_number = 0
        self.webcam = cv2.VideoCapture(self.camera_number)

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.__get_image_from_camera()

    def __get_image_from_camera(self):
        print('Start receive image ...')
        while True:
            ret,input_image = self.webcam.read()
            if ret:
                input_image = cv2.resize(input_image,(640,480))
                self.image_storage.set_input_image(input_image)
            else:
                break
        print('Stop receive image ...')
        self.webcam.release()

    def set_camera_number(self,number):
        self.camera_number = number

