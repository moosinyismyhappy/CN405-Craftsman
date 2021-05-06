import threading
from threading import Thread
import cv2
from PyQt5 import QtGui


class TestInputVideo(Thread):

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.camera_number = 0
        self.webcam = cv2.VideoCapture(self.camera_number)
        self.x = 100
        self.y = 100

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.__get_image_from_camera()

    def __get_image_from_camera(self):
        print('Start receive image ...')
        while True:
            ret, input_image = self.webcam.read()
            if ret:
                input_image = cv2.resize(input_image, (640, 480))
                input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
                # Convert RGB image to QImage form
                h, w, ch = input_image.shape
                bytesPerLine = ch * w
                converted_input_image = QtGui.QImage(input_image.data, w, h, bytesPerLine,
                                                     QtGui.QImage.Format_RGB888)
                self.gui.display_image_to_tracking_zone(self.x, self.y)

                self.x = self.x + 5
                self.y = self.y + 5
            else:
                break
        print('Stop receive image ...')
        self.webcam.release()
