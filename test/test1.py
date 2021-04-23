# Add new tracking method

import cv2
import numpy as np
import math

# Configuration
file_name = '../resources/videos/Test_Working.mp4'
black_img = cv2.imread('../resources/images/black_background.png')
detect_area = 1000
lower_value = 0.7
upper_value = 1.3
imageFrame = None
hsvFrame = None

# For left hand
hsv_lower_left = [-1, -1, -1, -1]
hsv_upper_left = [-1, -1, -1, -1]
center_bound_left = [-1, -1, -1, -1]
is_first_detect_left = True
prev_left = -1
curr_left = -1
prev_status_left = -1
curr_status_left = -1

# For right hand
hsv_lower_right = [-1, -1, -1, -1]
hsv_upper_right = [-1, -1, -1, -1]
center_bound_right = [-1, -1, -1, -1]
is_first_detect_right = True
prev_right = -1
curr_right = -1
prev_status_right = -1
curr_status_right = -1


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

    elif event == cv2.EVENT_RBUTTONDOWN:
        hsv_lower_right = adjust_lower_hsv(hsvFrame[y, x])
        hsv_upper_right = adjust_upper_hsv(hsvFrame[y, x])

def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def point_track_left(x,y):
    global prev_left, curr_left, image_frame, prev_status_left, curr_status_left , black_img
    prev_left = curr_left
    curr_left = x, y
    prev_status = curr_status_left

    diff_x = curr_left[0] - prev_left[0]
    diff_y = curr_left[1] - prev_left[1]

    result = degree(math.atan2(diff_y, diff_x))

    ##################
    #  Q2   270   Q1 #
    # 180        000 #
    #  Q3   090   Q4 #
    ##################

    if result >= 260 and result < 280:
        print('UP')
        curr_status_left = 0.5

    elif result >= 280 and result < 350:
        print('Q1')
        curr_status_left = 1

    elif result >= 350 and result < 360:
        print('RIGHT')
        curr_status_left = 1.5

    elif result >= 0 and result < 10:
        print('RIGHT')
        curr_status_left = 1.5

    elif result >= 10 and result < 80:
        print('Q4')
        curr_status_left = 4

    elif result >= 80 and result < 100:
        print('DOWN')
        curr_status_left = 4.5

    elif result >= 100 and result < 170:
        print('Q3')
        curr_status_left = 3

    elif result >= 170 and result < 190:
        print('LEFT')
        curr_status_left = 3.5

    elif result >= 190 and result < 260:
        print('Q2')
        curr_status_left = 2

    if curr_status_left != prev_status_left:
        cv2.circle(black_img, (x, y), 2, (0, 0, 255), 2)


def tracking_left(new_center):
    global imageFrame, center_bound_left,is_first_detect_left
    # x,y of center
    temp_x, temp_y = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = center_bound_left[0], center_bound_left[1], center_bound_left[2], center_bound_left[3]

    if temp_x>=x1 and temp_x<=x2 and temp_y>=y1 and temp_y<=y2:
        pass

    else:
        point_track_left(temp_x,temp_y)
        is_first_detect_left = True

def tracking_right(new_center):
    global imageFrame, center_bound_right,is_first_detect_right
    # x,y of center
    temp_x, temp_y = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = center_bound_right[0], center_bound_right[1], center_bound_right[2], center_bound_right[3]

    if temp_x>=x1 and temp_x<=x2 and temp_y>=y1 and temp_y<=y2:
        pass

    else:
        point_track_right(temp_x,temp_y)
        is_first_detect_right = True

def point_track_right(x,y):
    global prev_right, curr_right, image_frame, prev_status_right, curr_status_right , black_img
    prev_right = curr_right
    curr_right = x, y
    prev_status_right = curr_status_right

    diff_x = curr_right[0] - prev_right[0]
    diff_y = curr_right[1] - prev_right[1]

    result = degree(math.atan2(diff_y, diff_x))

    ##################
    #  Q2   270   Q1 #
    # 180        000 #
    #  Q3   090   Q4 #
    ##################

    if result >= 260 and result < 280:
        print('UP')
        curr_status_right = 0.5

    elif result >= 280 and result < 350:
        print('Q1')
        curr_status_right = 1

    elif result >= 350 and result < 360:
        print('RIGHT')
        curr_status_right = 1.5

    elif result >= 0 and result < 10:
        print('RIGHT')
        curr_status_right = 1.5

    elif result >= 10 and result < 80:
        print('Q4')
        curr_status_right = 4

    elif result >= 80 and result < 100:
        print('DOWN')
        curr_status_right = 4.5

    elif result >= 100 and result < 170:
        print('Q3')
        curr_status_right = 3

    elif result >= 170 and result < 190:
        print('LEFT')
        curr_status_right = 3.5

    elif result >= 190 and result < 260:
        print('Q2')
        curr_status_right = 2

    if curr_status_right != prev_status_right:
        cv2.circle(black_img, (x, y), 2, (0, 255, 255), 2)



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

                if is_first_detect_left:
                    center_bound_left = [x, y, x + w, y + h]
                    curr_left = x,y
                    prev_left = x,y
                    is_first_detect_left = False

                else:
                    imageFrame = cv2.rectangle(imageFrame, (center_bound_left[0], center_bound_left[1]),
                                               (center_bound_left[2], center_bound_left[3]),
                                               (0, 255, 0), 2)

                center = int((2 * x + w) / 2), int((2 * y + h) / 2)
                tracking_left(center)
                imageFrame = cv2.circle(imageFrame, center, 2, (0, 0, 255), 2)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 0, 255), 2)

                cv2.putText(imageFrame, "Detected Left", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        color_mask2 = cv2.dilate(color_mask2, kernal)
        resultColor2 = cv2.bitwise_and(hsvFrame, hsvFrame,
                                       mask=color_mask1)

        contours, hierarchy = cv2.findContours(color_mask2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area > detect_area):
                x, y, w, h = cv2.boundingRect(contour)

                if is_first_detect_right:
                    center_bound_right = [x, y, x + w, y + h]
                    curr_right = x, y
                    prev_right = x, y
                    is_first_detect_right = False

                else:
                    imageFrame = cv2.rectangle(imageFrame, (center_bound_right[0], center_bound_right[1]),
                                               (center_bound_right[2], center_bound_right[3]),
                                               (0, 255, 0), 2)

                center = int((2 * x + w) / 2), int((2 * y + h) / 2)
                tracking_right(center)
                imageFrame = cv2.circle(imageFrame, center, 2, (0, 255, 255), 2)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 255), 2)

                cv2.putText(imageFrame, "Detected Right", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))

        cv2.imshow("Multiple color Detection", imageFrame)
        cv2.imshow("Result", black_img)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
