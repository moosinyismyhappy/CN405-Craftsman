import inputVideo
import outputVideo
from inputVideo import *
from outputVideo import *

thread1 = inputVideo(0)
thread1.start()

thread2 = outputVideo(thread1)
thread2.start()