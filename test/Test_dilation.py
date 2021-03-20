import cv2
import numpy as np

img = cv2.imread('../resources/Images/original.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 100, 200)

kernel = np.ones((5,5),np.uint8)

dilation = cv2.dilate(edges,kernel,iterations = 1)

cv2.imshow('frame', dilation)

cv2.waitKey(0)
