import cv2
import threading
from threading import Thread

class inputVideo(Thread):

    def __init__(self, src_num):
        super().__init__()
        self.video_src = cv2.VideoCapture(src_num)
        self.stream_image = None
        self.camera_status = True
        self.hsv_image = None

    # set to private method
    def __save_stream_image(self):

        print('Start save stream images ...')

        # Always do when camera open
        while self.camera_status:

            if self.video_src.isOpened():

                ret, self.stream_image = self.video_src.read()

                # ret is flag to check that is still have images
                if not ret:
                    self.camera_status = False
                    break

            else:
                self.camera_status = False
                break

        print("Stop Saving images!")
        self.video_src.release()

    def get_stream_image(self):
        return self.stream_image

    def set_camera_status(self,statusVal):
        self.camera_status = statusVal

    def get_hsv_image(self):
        self.hsv_image = cv2.cvtColor(self.get_stream_image(), cv2.COLOR_BGR2HSV)
        return self.hsv_image

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        # Start method save_stream_image with thread
        self.__save_stream_image()