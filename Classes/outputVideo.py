import cv2
import threading
from threading import Thread

class outputVideo(Thread):

    def __init__(self, inputVid):
        super().__init__()
        self.inputVideo = inputVid

    def __show_stream_image(self):

        print('start show video ...')

        while True:

            # hsv_frame = cv2.cvtColor(self.stream_image, cv2.COLOR_BGR2HSV)

            try:
                cv2.imshow('Multiple color detection', self.inputVideo.get_stream_image())

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
