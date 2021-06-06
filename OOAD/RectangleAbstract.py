from abc import ABC,abstractmethod

class RectangleAbstract(ABC):

    @abstractmethod
    def get_update(self,value):
        pass