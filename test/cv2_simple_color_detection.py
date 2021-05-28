# Add new tracking method
import cv2
import numpy as np
import math

# Configuration
file_name = '../resources/videos/Full_Working1.mp4'
black_img = cv2.imread('../resources/images/transparent.png')
detect_area = 1000
lower_value = 0.7
upper_value = 1.3
imageFrame = None
hsvFrame = None

# For left hand
hsv_lower_left = [-1, -1, -1, -1]
hsv_upper_left = [-1, -1, -1, -1]
center_bound_left = [-1, -1, -1, -1]
is_first_detect_left = 0
prev_left = -1
curr_left = -1
prev_status_left = -1
curr_status_left = -1
is_out_left = False

# For right hand
hsv_lower_right = [-1, -1, -1, -1]
hsv_upper_right = [-1, -1, -1, -1]
center_bound_right = [-1, -1, -1, -1]
is_first_detect_right = 0
prev_right = -1
curr_right = -1
prev_status_right = -1
curr_status_right = -1
is_out_right = False


def set_max_value(input_val):
    if (input_val > 255):
        input_val = 255
    return input_val


def adjust_lower_hsv(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(int(i * lower_value))
    return temp_list


def adjust_upper_hsv(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(int(set_max_value(i * upper_value)))
    return temp_list


def mouse_click(event, x, y, flags, param):
    global hsv_lower_left, hsv_upper_left, hsv_lower_right, hsv_upper_right

    # Left Click to get HSV color value from image
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_lower_left = adjust_lower_hsv(hsvFrame[y, x])
        hsv_upper_left = adjust_upper_hsv(hsvFrame[y, x])

    if event == cv2.EVENT_RBUTTONDOWN:
        hsv_lower_right = adjust_lower_hsv(hsvFrame[y, x])
        hsv_upper_right = adjust_upper_hsv(hsvFrame[y, x])


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(file_name)
    # webcam = cv2.VideoCapture(0)
    while True:
        # Receive stream image from camera
        _, imageFrame = webcam.read()
        imageFrame = cv2.resize(imageFrame, (640, 480))
        # imageFrame = cv2.flip(imageFrame, 1)

        # Change color space from RGB to HSV
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        color_lower1 = np.array([hsv_lower_left[0], hsv_lower_left[1], hsv_lower_left[2]], np.uint8)
        color_upper1 = np.array([hsv_upper_left[0], hsv_upper_left[1], hsv_upper_left[2]], np.uint8)
        color_mask1 = cv2.inRange(hsvFrame, color_lower1, color_upper1)

        color_lower2 = np.array([hsv_lower_right[0], hsv_lower_right[1], hsv_lower_right[2]], np.uint8)
        color_upper2 = np.array([hsv_upper_right[0], hsv_upper_right[1], hsv_upper_right[2]], np.uint8)
        color_mask2 = cv2.inRange(hsvFrame, color_lower2, color_upper2)

        kernal = np.ones((5, 5), "int8")
        color_mask1 = cv2.dilate(color_mask1, kernal)
        resultColor1 = cv2.bitwise_and(hsvFrame, hsvFrame,
                                       mask=color_mask1)
        contours, hierarchy = cv2.findContours(color_mask1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detect_area):
                x, y, w, h = cv2.boundingRect(contour)
                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                imageFrame = cv2.circle(imageFrame, center, 2, (0, 0, 255), 2)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 0, 255), 2)
                cv2.putText(imageFrame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 0, 255))

        color_mask2 = cv2.dilate(color_mask2, kernal)
        resultColor2 = cv2.bitwise_and(hsvFrame, hsvFrame,
                                       mask=color_mask2)
        contours, hierarchy = cv2.findContours(color_mask2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detect_area):
                x, y, w, h = cv2.boundingRect(contour)
                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                imageFrame = cv2.circle(imageFrame, center, 2, (0, 255, 255), 2)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 255), 2)
                cv2.putText(imageFrame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 255))

        final_image = cv2.addWeighted(imageFrame, 1.0, black_img, 1.0, 0)
        cv2.imshow("Multiple color Detection", final_image)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
