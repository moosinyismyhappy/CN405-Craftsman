import cv2


class Rectangle(RectangleAbstract):

    def __init__(self,image,x1,y1,x2,y2):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.image = image

    def get_update(self,value):
        x1 = value[0]
        y1 = value[1]
        x2 = value[2]
        y2 = value[3]
        cv2.rectangle(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)

