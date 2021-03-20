import cv2
from threading import Thread
import threading

class InputVideo(Thread):

    # Class Constructor
    def __init__(self, src_video_number, input_videoStatus):
        Thread.__init__(self)
        self.webcam = cv2.VideoCapture(src_video_number)
        self.video_status = input_videoStatus

        # set initial frame to null
        self.frame = None

    def is_there_frame(self):
        if self.frame is None:
            return False

        else:
            return True

    def getting_video(self):

        # video status to True for reading frame
        self.video_status.set_video_status(True)

        while self.video_status.check_video_status():

            ret, self.frame = self.webcam.read()

            if not ret:
                break

        self.webcam.release()

    def pass_video(self):
        return self.frame

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        self.getting_video()