import threading
import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage

class GuiOutputVideo(QThread):
    image_update = pyqtSignal(QImage)

    def __init__(self, input_video):
        super().__init__()
        self.input_video = input_video

    def get_image_from_camera(self):
        while self.input_video.get_camera_status():
            try:
                # Change color system BGR(OpenCV) to RGB(Qt)
                self.input_image_rgb = cv2.cvtColor(self.input_video.get_input_image(), cv2.COLOR_BGR2RGB)
            except:
                print('Waiting for image from InputVideo')
                continue
            # Convert RGB image to RGB888
            converted_rgb888_image = QImage(self.input_image_rgb.data, self.input_image_rgb.shape[1],
                                                self.input_image_rgb.shape[0], QImage.Format_RGB888)
            converted_image = converted_rgb888_image.scaled(640, 480, Qt.KeepAspectRatio)
            # Send signal to GuiController to show Picture
            self.image_update.emit(converted_image)

    def run(self):
        # Display Thread and Process ID
        self.get_image_from_camera()
