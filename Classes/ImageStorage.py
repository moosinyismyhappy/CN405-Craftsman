import cv2

class ImageStorage():

    def __init__(self):
        self.image = None
        self.hsv_image = None
        self.detected_image = None
        self.is_detected = False

    def add_image(self, input_image):
        temp_image = input_image
        self.image = temp_image.copy()

    def add_detected_image(self, input_image):
        self.detected_image = input_image
        self.is_detected = True

    def get_detected_image(self):
        return self.detected_image

    def get_detected_status(self):
        return self.is_detected

    def set_detected_status(self,statusVal):
        self.is_detected = statusVal

    def get_image(self):
        return self.image

    def get_hsv_image(self):
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return self.hsv_image
