import cv2
import numpy as np

img1 = cv2.imread('../resources/images/craftsman_hand.png')
img1 = cv2.resize(img1,(640,480))
img2 = cv2.imread('../resources/images/points.png')
img2 = cv2.resize(img2,(640,480))
dst = cv2.addWeighted(img1, 1.0, img2, 1.0, 0)

img_arr = np.hstack((img1, img2))
cv2.imshow('Input Images',img_arr)
cv2.imshow('Blended Image',dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
