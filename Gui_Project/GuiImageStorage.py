import cv2

class GuiImageStorage():

    def __init__(self):
        # Instance variable for images
        self.input_image = None
        self.hsv_image_for_detection = None
        self.detected_image = None
        self.transparent_image_for_detection = cv2.imread('../resources/images/test_transparent.png')
        self.transparent_image_for_tracking = cv2.imread('../resources/images/transparent.png')
        self.is_detected_status = False

        # other instance variable for process
        self.storage_status = False
        self.show_status = 0

    def set_detected_image_status(self,new_status):
        self.is_detected_status = new_status

    def get_detected_image_status(self):
        return self.is_detected_status

    def set_detected_image(self,new_image):
        self.detected_image = new_image

    def get_detect_image(self):
        return self.detected_image

    def set_hsv_image_for_detection(self,new_image):
        self.hsv_image_for_detection = new_image.copy()

    def get_hsv_image_for_detection(self):
        return self.hsv_image_for_detection

    def set_input_image(self,new_image):
        self.input_image = new_image.copy()

    def get_input_image(self):
        return self.input_image

    def get_transparent_image_for_detection(self):
        return self.transparent_image_for_detection.copy()

    def get_transparent_image_for_tracking(self):
        return self.transparent_image_for_tracking




