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

                input_image = cv2.rectangle(input_image,(100,100),(200,200),(0,255,0),3)

                # Change color system BGR(OpenCV) to RGB(Qt)
                self.input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
            except:
                print('Waiting for image from InputVideo')
                continue

            # Convert to QImage form
            h, w, ch = self.input_image_rgb.shape
            bytesPerLine = ch * w
            converted_image = QtGui.QImage(self.input_image_rgb.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)

            # send converted image back to gui
            self.gui.draw_image(converted_image)




