import threading
import cv2
from threading import Thread
from PyQt5 import QtGui

from OOAD.GrayProcess import GrayProcess
from OOAD.HSVProcess import HSVProcess
from OOAD.InputImage import InputImage
from OOAD.RGBProcess import RGBProcess


class GuiProcessOutput(Thread):
    def __init__(self, gui, image_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = image_storage
        self.converted_image = None

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.__processing_output()

    def __processing_output(self):
        while True:
            try:
                # get input image from image_storage
                input_image = self.image_storage.get_input_image()

                # Change color system BGR(OpenCV) to HSV
                hsv_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

                # Display track on screen
                if self.gui.get_toggle_track_status():
                    input_image = cv2.addWeighted(input_image, 0.9, self.image_storage.get_background_image_for_track(),
                                                  1.0, 0)

                # Display mark on screen
                if self.gui.get_toggle_mark_status():
                    input_image = cv2.addWeighted(input_image, 0.9, self.image_storage.get_background_image_for_mark(),
                                                  1.0, 0)

                # Send to image storage for color detection
                self.image_storage.set_hsv_image_for_detection(hsv_image)

                if self.gui.get_show_image_type() == 0:
                    image_for_decorate = RGBProcess(InputImage(self.image_storage))
                    self.converted_image = image_for_decorate.process()

                # image type = 1 is HSV
                elif self.gui.get_show_image_type() == 1:
                    image_for_decorate = HSVProcess(InputImage(self.image_storage))
                    self.converted_image = image_for_decorate.process()

                # image type = 2 is Grayscale
                elif self.gui.get_show_image_type() == 2:
                    image_for_decorate = GrayProcess(InputImage(self.image_storage))
                    self.converted_image = image_for_decorate.process()

            except:
                print('Cannot convert image ...')
                continue

            # Send image to gui for display image
            self.gui.display_image_to_camera_zone(self.converted_image)
