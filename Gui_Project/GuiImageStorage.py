import cv2


class GuiImageStorage():

    def __init__(self):
        self.input_image = None
        self.hsv_image = None
        self.hsv_image_for_detect = None
        self.rgb_image = None
        self.gray_image = None
        self.detected_image = None
        self.transparent_original_image = cv2.imread('../resources/images/transparent.png')
        self.transparent_image = self.transparent_original_image.copy()
        self.storage_status = False
        self.show_status = 0

    def get_transparent_image(self):
        return self.transparent_image

    def set_transparent_image(self,new_image):
        self.transparent_image = new_image

    def set_input_image(self, new_image):
        self.input_image = new_image.copy()

    def get_input_image(self):
        return self.input_image

    def set_detected_image(self, new_image):
        self.detected_image = new_image

    def get_detected_image(self):
        return self.detected_image

    def set_hsv_image_for_detect(self, new_image):
        self.hsv_image_for_detect = new_image

    def get_hsv_image_for_detect(self):
        return self.hsv_image_for_detect

    def set_rgb_image(self, new_image):
        self.rgb_image = new_image

    def get_rgb_image(self):
        return self.rgb_image

    def set_hsv_image(self, new_image):
        self.hsv_image = new_image

    def get_hsv_image(self):
        return self.hsv_image

    def set_gray_image(self, new_image):
        self.gray_image = new_image

    def get_gray_image(self):
        return self.gray_image

    def get_storage_status(self):
        return self.storage_status

    def set_storage_status(self, status):
        self.storage_status = status

    def set_show_status(self, status):
        self.show_status = status

    def get_show_image(self):
        if self.show_status == 0:
            return self.get_rgb_image()
        elif self.show_status == 1:
            return self.get_hsv_image()
        elif self.show_status == 2:
            return self.get_gray_image()
