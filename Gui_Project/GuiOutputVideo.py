import threading
import cv2
from threading import Thread
from PyQt5 import QtGui


class GuiOutputVideo(Thread):

    def __init__(self, gui, image_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = image_storage
        self.converted_image = None
        self.detected_image = None

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
                # Send to image storage for color detection
                self.image_storage.set_hsv_image_for_detection(hsv_image)

                if self.gui.get_show_image_type() == 0:
                    # Change color system BGR(OpenCV) to RGB
                    rgb_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

                    # Convert RGB image to QImage form
                    h, w, ch = rgb_image.shape
                    bytesPerLine = ch * w
                    converted_rgb_image = QtGui.QImage(rgb_image.data, w, h, bytesPerLine,
                                                       QtGui.QImage.Format_RGB888)
                    self.converted_image = converted_rgb_image

                # image type = 1 is HSV
                elif self.gui.get_show_image_type() == 1:

                    # Convert HSV image to QImage form
                    h, w, ch = hsv_image.shape
                    bytesPerLine = ch * w
                    converted_hsv_image = QtGui.QImage(hsv_image.data, w, h, bytesPerLine,
                                                       QtGui.QImage.Format_RGB888)
                    self.converted_image = converted_hsv_image

                # image type = 2 is Grayscale
                elif self.gui.get_show_image_type() == 2:
                    # Change color system BGR(OpenCV) to Grayscale
                    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

                    # Convert to QImage form
                    h, w = grayscale_image.shape
                    bytesPerLine = w
                    converted_grayscale_image = QtGui.QImage(grayscale_image.data, w, h, bytesPerLine,
                                                             QtGui.QImage.Format_Grayscale8)
                    self.converted_image = converted_grayscale_image

            except:
                print('Cannot convert image ...')
                continue

            # Send image to gui for display image
            self.gui.display_image_to_camera_zone(self.converted_image)