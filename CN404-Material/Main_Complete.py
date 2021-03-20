import threading
import time
from threading import Thread

import cv2
import numpy as np

# Global variable
image_frame = None
hsv_frame = None
is_read_video = True


class get_input_video(Thread):

    def __init__(self, source_camera_number):
        super().__init__()
        self.camera = cv2.VideoCapture(source_camera_number)

    def save_image_frame(self):

        global image_frame

        print('saving stream images ...')

        while is_read_video:

            ret, input_image = self.camera.read()

            if not ret:
                break

            else:
                image_frame = input_image

        print("Stop Saving Image.")
        self.camera.release()

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        # Start function save_image_frame with thread
        self.save_image_frame()


class show_video(Thread):
    def __init__(self):
        super().__init__()
        pass

    def show(self):

        global image_frame, is_read_video, hsv_frame

        print('Showing video ...')

        # Set Mouse callback for window
        cv2.namedWindow('Multiple color detection')
        CheckEvent('Multiple color detection').setMouseCallback()

        while is_read_video:

            hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

            cv2.imshow('Multiple color detection', image_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        # Stop Camera
        is_read_video = False

    def run(self):

        # Display Thread and Process ID
        print(threading.current_thread())

        # Start show video with thread
        self.show()


class CheckEvent:

    def __init__(self, setWindowName):
        self.windowName = setWindowName
        self.color_thread_1 = color_detection()
        self.color_thread_2 = color_detection()

        self.count_click_color_1 = 0
        self.count_click_color_2 = 0

    # Private function
    def __getMouseCallback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:

            self.count_click_color_1 = self.count_click_color_1 + 1

            if self.count_click_color_1 == 1:
                self.color_thread_1.start()
                hsv_list = hsv_frame[y, x]
                self.color_thread_1.setDetectColor(hsv_list[0], hsv_list[1], hsv_list[2])

            else:
                self.count_click_color_1 = -1
                hsv_list = hsv_frame[y, x]
                self.color_thread_1.setDetectColor(hsv_list[0], hsv_list[1], hsv_list[2])

        if event == cv2.EVENT_RBUTTONDOWN:

            self.count_click_color_2 = self.count_click_color_2 + 1

            if self.count_click_color_2 == 1:
                self.color_thread_2.start()
                hsv_list = hsv_frame[y, x]
                self.color_thread_2.setDetectColor(hsv_list[0], hsv_list[1], hsv_list[2])

            else:
                self.count_click_color_2 = -1
                hsv_list = hsv_frame[y, x]
                self.color_thread_2.setDetectColor(hsv_list[0], hsv_list[1], hsv_list[2])

    def setMouseCallback(self):
        cv2.setMouseCallback(self.windowName, self.__getMouseCallback)


class color_detection(Thread):

    def __init__(self):
        super().__init__()

        # Set lower for HSV
        self.lower_hue = 0
        self.lower_sat = 0
        self.lower_val = 0

        # Set lower for HSV
        self.upper_hue = 0
        self.upper_sat = 0
        self.upper_val = 0

        # Set range (lower and upper)
        self.range = 0.15

        # Set frame count for optimize detection
        self.count_frame = 0
        self.count_frame_max = 10
        self.count_detect = 0

        # Detect area List[]
        self.detected_area = None

    def setDetectColor(self, hVal, sVal, vVal):

        self.lower_hue = int(hVal * (1 - self.range))
        self.lower_sat = int(sVal * (1 - self.range))
        self.lower_val = int(vVal * (1 - self.range))

        self.upper_hue = int(hVal * (1 + self.range))
        self.upper_sat = int(sVal * (1 + self.range))
        self.upper_val = int(vVal * (1 + self.range))

        if (self.lower_hue <= 0):
            self.lower_hue = 0

        if (self.lower_sat <= 0):
            self.lower_sat = 0

        if (self.lower_val <= 0):
            self.lower_val = 0

        if (self.upper_hue >= 255):
            self.upper_hue = 255

        if (self.upper_sat >= 255):
            self.upper_sat = 255

        if (self.upper_val >= 255):
            self.upper_val = 255

    def detect_color_area(self):

        global hsv_frame, image_frame

        print('Detecting color ...')

        while is_read_video:

            color_lower = np.array([self.lower_hue, self.lower_sat, self.lower_val])
            color_upper = np.array([self.upper_hue, self.upper_sat, self.upper_val])
            color_mask = cv2.inRange(hsv_frame, color_lower, color_upper)

            kernal = np.ones((5, 5), "uint8")

            color_mask = cv2.dilate(color_mask, kernal)

            contours, hierarchy = cv2.findContours(color_mask,
                                                   cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 3000:
                    x, y, w, h = cv2.boundingRect(contour)

                    self.detected_area = [x, y, w, h]

                    self.count_detect += 1

            if self.count_frame == self.count_frame_max and self.count_detect >= (self.count_frame / 2):
                cv2.rectangle(image_frame, (self.detected_area[0], self.detected_area[1]),
                              (self.detected_area[0] + self.detected_area[2],
                               self.detected_area[1] + self.detected_area[3]),
                              (0, 255, 0), 2)

            if self.count_frame == self.count_frame_max:
                self.count_frame = 0
                self.count_detect = 0

            self.count_frame += 1

    def run(self):
        time.sleep(0.5)

        # Display Thread and Process ID
        print(threading.current_thread())

        # Start color detection thread
        self.detect_color_area()


if __name__ == "__main__":
    # get video thread
    get_video_thread = get_input_video(0)
    get_video_thread.start()

    time.sleep(1)

    show_video_thread = show_video()
    show_video_thread.start()