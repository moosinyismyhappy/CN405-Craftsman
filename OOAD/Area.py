from OOAD.AreaController import AreaController


class Area(AreaController):

    def __init__(self):
        self.rect_list = []

    def add(self,rect):
        self.rect_list.append(rect)

    def remove(self,rect):
        self.rect_list.remove(rect)

    def update(self,value):
        for i in self.rect_list:
            i.get_update(value)