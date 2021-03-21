import cv2
import threading
from threading import Thread
from mouseDetection import *


class outputVideo(Thread):

    def __init__(self, inputVid):
        super().__init__()
        self.inputVideo = inputVid

        # Create mouseDetection
        self.mouse = mouseDetection()

        self.window_name = 'Multiple color detection'

    def __show_stream_image(self):

        print('start show video ...')

        while True:

            try:
                cv2.imshow(self.window_name, self.inputVideo.get_stream_image())
                self.mouse.start_mouse_detection(self.window_name, self.inputVideo.get_hsv_image())

            except Exception:
                print('Connecting ...')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.inputVideo.set_camera_status(False)
                break

        cv2.destroyAllWindows()

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.__show_stream_image()
