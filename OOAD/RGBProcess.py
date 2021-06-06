import cv2
from PyQt5 import QtGui

from OOAD.ImageDecorator import ImageDecorator


class RGBProcess(ImageDecorator):
    def __init__(self,image):
        super().__init__(image)

    def process(self):
        self.image.process()
        self.rgb_process()

    def rgb_process(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        # Convert RGB image to QImage form
        h, w, ch = rgb_image.shape
        bytesPerLine = ch * w
        converted_rgb_image = QtGui.QImage(rgb_image.data, w, h, bytesPerLine,
                                           QtGui.QImage.Format_RGB888)
        return converted_rgb_image
