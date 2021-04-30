class GuiImageStorage():

    def __init__(self):
        self.input_image = None
        self.hsv_image = None
        self.storage_status = False

    def set_input_image(self,new_image):
        self.input_image = new_image.copy()

    def get_input_image(self):
        return self.input_image

    def set_hsv_image(self,new_image):
        self.hsv_image = new_image.copy()

    def get_hsv_image(self):
        return self.hsv_image

    def get_storage_status(self):
        return self.storage_status

    def set_storage_status(self,status):
        self.storage_status = status

