from abc import ABC, abstractmethod


class ImageProcessing(ABC):
    @abstractmethod
    def process(self):
        pass
