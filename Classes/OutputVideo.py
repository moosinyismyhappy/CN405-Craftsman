import cv2
import threading
from threading import Thread
from MouseDetection import *


class OutputVideo(Thread):

    def __init__(self, input_vid, input_storage):
        super().__init__()
        self.image_storage = input_storage
        self.input_video = input_vid
        self.window_name = 'Multiple color detection'

        # Create mouseDetection
        self.mouse_detection = MouseDetection(self.image_storage)

    def __show_stream_image(self):
        print('start show video ...')
        while True:
            try:
                # Check image is detected or not?
                if not self.image_storage.get_detected_status():
                    cv2.imshow(self.window_name, self.image_storage.get_image())
                else:
                    cv2.imshow(self.window_name, self.image_storage.get_detected_image())
                    self.image_storage.set_detected_status(False)

            except Exception:
                print('Exception from __show_stream_image Class OutputVideo')
                continue

            # Do this section when no exception occur
            self.mouse_detection.start_mouse_detection(self.window_name)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.input_video.set_camera_status(False)
                break

        cv2.destroyAllWindows()

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.__show_stream_image()
