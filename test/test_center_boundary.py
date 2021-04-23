# Test Tracking with new method

import cv2
import numpy as np

file_name = '../resources/videos/Full_Working1.mp4'
detect_area = 1000
lower_value = 0.7
upper_value = 1.3

is_left_first = True
prev_left = -1
curr_left = -1
prev_status_left = None
curr_status_left = None
center_boundary_left = None
is_in_boundary_left = False

is_right_first = True
prev_right = -1
curr_right = -1
prev_status_right = None
curr_status_right = None

count = 0
imageFrame = None
hsvFrame = None
hsv_upper_left = [-1, -1, -1]
hsv_lower_left = [-1, -1, -1]
hsv_upper_right = [-1, -1, -1]
hsv_lower_right = [-1, -1, -1]


def trackingLeft(input):
    global is_left_first, prev_left, curr_left, prev_status_left, curr_status_left, imageFrame,center_boundary_left

    x_center = input[0]
    y_center = input[1]

    x1 = center_boundary_left[0]
    x2 = center_boundary_left[2]
    y1 = center_boundary_left[1]
    y2 = center_boundary_left[3]

    if not x_center>=x1 and x_center<=x2 and y_center>=y1 and y_center<=y2 :
        print('not in')
        center_boundary_left = [50,50,100,100]
        imageFrame = cv2.rectangle(imageFrame, (x1, y1),
                                   (x2, y2),
                                   (0, 255, 0), 2)

    else:
        imageFrame = cv2.rectangle(imageFrame, (x1, y1),
                                   (x2, y2),
                                   (0, 255, 0), 2)

def trackingRight(input):
    global is_right_first, prev_right, curr_right, prev_status_right, curr_status_right


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
    global is_left_first, prev, curr, prev_status, curr_status, hsv_lower_left, hsv_upper_left, hsv_lower_right, hsv_upper_right

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

    while True:

        # Receive stream image from camera
        _, imageFrame = webcam.read()

        imageFrame = cv2.resize(imageFrame, (800, 600))

        # Change color space from RGB to HSV
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        color_lower1 = np.array([hsv_lower_left[0], hsv_lower_left[1], hsv_lower_left[2]], np.uint8)
        color_upper1 = np.array([hsv_upper_left[0], hsv_upper_left[1], hsv_upper_left[2]], np.uint8)
        color_mask1 = cv2.inRange(hsvFrame, color_lower1, color_upper1)

        color_lower2 = np.array([hsv_lower_right[0], hsv_lower_right[1], hsv_lower_right[2]], np.uint8)
        color_upper2 = np.array([hsv_upper_right[0], hsv_upper_right[1], hsv_upper_right[2]], np.uint8)
        color_mask2 = cv2.inRange(hsvFrame, color_lower2, color_upper2)

        kernal = np.ones((5, 5), "uint8")

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

                imageFrame = cv2.circle(imageFrame, center, 2, (255, 255, 0), 2)

                if is_in_boundary_left:
                    trackingLeft(center)

                else:
                    center_boundary_left = [x,y,x+w,y+h]
                    print('not in boundary', center_boundary_left)
                    is_in_boundary_left = True

                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                """imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                cv2.putText(imageFrame, "Detected Left", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))"""

        contours, hierarchy = cv2.findContours(color_mask2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detect_area):
                x, y, w, h = cv2.boundingRect(contour)

                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                if not is_right_first:
                    prev_right = curr_right
                    curr_right = center
                    prev_status_right = curr_status_right

                    if prev_right == curr_right:
                        continue

                    trackingRight(center)

                else:
                    curr_right = center
                    prev_right = center
                    prev_status_right = (0, 0)
                    curr_status_right = (0, 0)
                    # print('First Time Right', prev_right, curr_right, prev_status_right, curr_status_right)
                    is_right_first = False

                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 0), 2)

                imageFrame = cv2.circle(imageFrame, center, 2, (255, 255, 0), 2)

                cv2.putText(imageFrame, "Detected Right", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        cv2.imshow("Multiple color Detection", imageFrame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
