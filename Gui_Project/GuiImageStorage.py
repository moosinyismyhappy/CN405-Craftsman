import cv2


class GuiImageStorage():
    def __init__(self):
        # Instance variable for images
        self.input_image = None
        self.hsv_image_for_detection = None
        self.background_image_for_track = cv2.imread('../resources/images/transparent.png')

    def set_hsv_image_for_detection(self, new_image):
        self.hsv_image_for_detection = new_image.copy()

    def get_hsv_image_for_detection(self):
        return self.hsv_image_for_detection

    def set_input_image(self, new_image):
        self.input_image = new_image.copy()

    def get_input_image(self):
        return self.input_image
