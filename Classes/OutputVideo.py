import cv2
from threading import Thread
import threading

class showVideo(Thread):

    # Class Constructor
    def __init__(self, input_getVideo, input_videoStatus):
        Thread.__init__(self)
        self.get_video = input_getVideo
        self.video_status = input_videoStatus

    def showing_video(self):

        while True:

            if self.get_video.is_there_frame():

                cv2.imshow('frame', self.get_video.pass_video())

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    # Set video status to False to terminate getVideo
                    self.video_status.set_video_status(False)

                    # break showing video
                    break

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        self.showing_video()