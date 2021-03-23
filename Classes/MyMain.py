import InputVideo
import OutputVideo
from InputVideo import *
from OutputVideo import *
from ImageStorage import *

image_storage = ImageStorage()

thread1 = InputVideo(0, image_storage)
thread1.start()

thread2 = OutputVideo(thread1, image_storage)
thread2.start()