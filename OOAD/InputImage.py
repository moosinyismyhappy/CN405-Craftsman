from OOAD.ImageProcessing import ImageProcessing


class InputImage(ImageProcessing):

    def __init__(self, image_storage):
        self.image_storage = image_storage

    def process(self):
        self.image = self.image_storage.get_input_image()
