from abc import ABC,abstractmethod

class AreaController(ABC):

    @abstractmethod
    def add(self,rect):
        pass

    @abstractmethod
    def remove(self,rect):
        pass

    @abstractmethod
    def update(self,value):
        pass
