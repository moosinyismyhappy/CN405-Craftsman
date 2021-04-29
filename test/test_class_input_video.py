import cv2
import threading
from threading import Thread


class InputVideo(Thread):

    def __init__(self, src_num):
        super().__init__()
        self.video_src = cv2.VideoCapture(src_num)
        self.image = None
        self.camera_status = True

    # set to private method
    def __save_stream_image(self):
        print('Start save stream images ...')

        # always do when camera open
        while self.camera_status:
            if self.video_src.isOpened():
                ret, self.image = self.video_src.read()

                # Resize image to 640x480
                self.image = cv2.resize(self.image, (640, 480))

                # ret is flag to check that is still have images
                if not ret:
                    self.camera_status = False
                    break

        print("Stop Saving images!")
        self.video_src.release()

    def get_image(self):
        return self.image

    def set_camera_status(self, statusVal):
        self.camera_status = statusVal

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # Start method save_stream_image with thread
        self.__save_stream_image()
