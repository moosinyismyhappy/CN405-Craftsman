from OOAD.ImageProcessing import ImageProcessing


class ImageDecorator(ImageProcessing):

    def __init__(self,image):
        self.image = image

    def process(self):
        self.image.process()