import threading
import cv2
from threading import Thread
from PyQt5 import QtGui


class GuiOutputVideo(Thread):

    def __init__(self, gui, image_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = image_storage

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.__processing_output()

    def __processing_output(self):
        while self.image_storage.get_storage_status():
            try:
                # get input image from image_storage
                input_image = self.image_storage.get_input_image()

                # Change color system BGR(OpenCV) to HSV for Detection
                self.hsv_image_for_detect = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

                # Change color system BGR(OpenCV) to RGB(Qt)
                self.input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

                # Change color system BGR(OpenCV) to HSV
                self.input_image_hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

                # Change color system BGR(OpenCV) to HSV for Detection
                self.input_image_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

            except:
                print('Waiting for image from InputVideo')
                continue

            # add converted hsv image to image storage
            self.image_storage.set_hsv_image_for_detect(self.hsv_image_for_detect)

            # Convert to QImage form
            h, w, ch = self.input_image_rgb.shape
            bytesPerLine = ch * w
            converted_rgb_image = QtGui.QImage(self.input_image_rgb.data, w, h, bytesPerLine,
                                               QtGui.QImage.Format_RGB888)

            # Convert to QImage form
            h, w, ch = self.input_image_hsv.shape
            bytesPerLine = ch * w
            converted_hsv_image = QtGui.QImage(self.input_image_hsv.data, w, h, bytesPerLine,
                                               QtGui.QImage.Format_RGB888)

            # Convert to QImage form
            h, w = self.input_image_gray.shape
            bytesPerLine = w
            converted_gray_image = QtGui.QImage(self.input_image_gray.data, w, h, bytesPerLine,
                                                QtGui.QImage.Format_Grayscale8)

            # add converted hsv image to image storage
            self.image_storage.set_hsv_image(converted_hsv_image)

            # add converted rgb image to image storage
            self.image_storage.set_rgb_image(converted_rgb_image)

            # add converted rgb image to image storage
            self.image_storage.set_gray_image(converted_gray_image)

            # send converted image back to gui
            self.gui.show_image_to_screen(self.image_storage.get_show_image())
