from OutputVideo import *
from ImageStorage import *
from InputVideo import *

if __name__ == "__main__":

    image_storage = ImageStorage()

    thread1 = InputVideo(0, image_storage)
    thread1.start()

    thread2 = OutputVideo(thread1, image_storage)
    thread2.start()