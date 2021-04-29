import cv2
import threading
from threading import Thread

from PyQt5 import Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage


class OutputVideo(Thread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, input_video):
        super().__init__()
        self.input_video = input_video
        self.window_name = 'Multiple color detection'

    def __show_stream_image(self):
        print('start show video ...')

        while True:
            try:
                print(self.input_video.get_image())
                """
                self.image = cv2.cvtColor(self.input_video.get_image(), cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)"""

            except Exception:
                print('Exception from __show_stream_image Class OutputVideo')
                continue

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.__show_stream_image()
