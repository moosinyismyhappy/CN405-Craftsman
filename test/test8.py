import cv2
import numpy as np
import threading
import time

# Configuration
file_name = '../resources/videos/Full_Working2.mp4'
black_img = cv2.imread('../resources/images/transparent.png')
detect_area = 1000
lower_value = 0.7
upper_value = 1.3
image_frame = None
hsv_frame = None

# area position
# input1 192 51 245 141
# input2 268 228 402 350
# output 504 173 627 276
# work 264 48 490 162
input1_area = [192, 51, 245, 141]
input2_area = [268, 228, 402, 350]
output_area = [504, 173, 627, 276]
work_area = [264, 48, 490, 162]
current_area = -1
timer_button = False

# input1 timer
input1_start_time = 0
input1_end_time = 0
input1_timer_status = -1

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


def input1_timer():
    global timer_button
    global current_area, previous_area
    global input1_timer_status, input1_start_time, input1_end_time

    print(threading.current_thread())

    while True:

        # for this loop can run without lag
        time.sleep(0)

        # check timer button
        if timer_button is True:

            if current_area == 4:
                if input1_timer_status == -1:
                    # enable timer for input1
                    input1_timer_status = 0
                elif input1_timer_status == 1:
                    input1_end_time = time.time()
                    print('end timer ', input1_end_time - input1_start_time)
                    input1_timer_status = 0

            elif current_area != 4 and input1_timer_status == 0:
                print('start timer')
                input1_start_time = time.time()
                input1_timer_status = 1


def where_is_center_in_area_left(center):
    global current_area

    x_text = center[0] - 15
    y_text = center[1] - 15

    if is_in_input1_area(center):
        cv2.putText(image_frame, 'In input1', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area = 1

    elif is_in_input2_area(center):
        cv2.putText(image_frame, 'In input2', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area = 2

    elif is_in_output_area(center):
        cv2.putText(image_frame, 'In output', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area = 3

    elif is_in_work_area(center):
        cv2.putText(image_frame, 'In work', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area = 4

    else:
        current_area = -1


def is_in_input1_area(center):
    x1 = input1_area[0]
    y1 = input1_area[1]
    x2 = input1_area[2]
    y2 = input1_area[3]

    # do when center inside input1 area
    if x1 < center[0] < x2 and y1 < center[1] < y2:
        return True
    else:
        return False


def is_in_input2_area(center):
    x1 = input2_area[0]
    y1 = input2_area[1]
    x2 = input2_area[2]
    y2 = input2_area[3]

    # do when center inside input2 area
    if x1 < center[0] < x2 and y1 < center[1] < y2:
        return True
    else:
        return False


def is_in_output_area(center):
    x1 = output_area[0]
    y1 = output_area[1]
    x2 = output_area[2]
    y2 = output_area[3]

    # do when center inside output area
    if x1 < center[0] < x2 and y1 < center[1] < y2:
        return True
    else:
        return False


def is_in_work_area(center):
    x1 = work_area[0]
    y1 = work_area[1]
    x2 = work_area[2]
    y2 = work_area[3]

    # do when center inside work area
    if x1 < center[0] < x2 and y1 < center[1] < y2:
        return True
    else:
        return False


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
    global timer_button
    global hsv_lower_left, hsv_upper_left, hsv_lower_right, hsv_upper_right

    # Left Click to get HSV color value from image
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_lower_left = adjust_lower_hsv(hsv_frame[y, x])
        hsv_upper_left = adjust_upper_hsv(hsv_frame[y, x])
        timer_button = True

    if event == cv2.EVENT_RBUTTONDOWN:
        hsv_lower_right = adjust_lower_hsv(hsv_frame[y, x])
        hsv_upper_right = adjust_upper_hsv(hsv_frame[y, x])


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(file_name)
    # webcam = cv2.VideoCapture(0)

    # start timer with thread
    thr = threading.Thread(target=input1_timer)
    thr.start()

    while True:
        # Receive stream image from camera
        _, image_frame = webcam.read()
        image_frame = cv2.resize(image_frame, (640, 480))

        # Change color space from RGB to HSV
        hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

        color_lower1 = np.array([hsv_lower_left[0], hsv_lower_left[1], hsv_lower_left[2]], np.uint8)
        color_upper1 = np.array([hsv_upper_left[0], hsv_upper_left[1], hsv_upper_left[2]], np.uint8)
        color_mask1 = cv2.inRange(hsv_frame, color_lower1, color_upper1)

        color_lower2 = np.array([hsv_lower_right[0], hsv_lower_right[1], hsv_lower_right[2]], np.uint8)
        color_upper2 = np.array([hsv_upper_right[0], hsv_upper_right[1], hsv_upper_right[2]], np.uint8)
        color_mask2 = cv2.inRange(hsv_frame, color_lower2, color_upper2)

        kernal = np.ones((5, 5), "int8")
        color_mask1 = cv2.dilate(color_mask1, kernal)
        resultColor1 = cv2.bitwise_and(hsv_frame, hsv_frame,
                                       mask=color_mask1)
        contours, hierarchy = cv2.findContours(color_mask1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > detect_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                cv2.circle(image_frame, center, 2, (0, 0, 255), 2)
                cv2.rectangle(image_frame, (x, y),
                              (x + w, y + h),
                              (0, 0, 255), 2)

                # find where area that center at
                where_is_center_in_area_left(center)

        color_mask2 = cv2.dilate(color_mask2, kernal)
        resultColor2 = cv2.bitwise_and(hsv_frame, hsv_frame,
                                       mask=color_mask2)
        contours, hierarchy = cv2.findContours(color_mask2,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > detect_area:
                x, y, w, h = cv2.boundingRect(contour)
                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                cv2.circle(image_frame, center, 2, (0, 255, 255), 2)
                cv2.rectangle(image_frame, (x, y),
                              (x + w, y + h),
                              (0, 255, 255), 2)

        # draw input1_area
        cv2.rectangle(image_frame, (192, 51), (245, 141), (0, 0, 255), 2)
        # draw input2_area
        cv2.rectangle(image_frame, (268, 228), (402, 350), (0, 150, 255), 2)
        # draw output_area
        cv2.rectangle(image_frame, (504, 173), (627, 276), (0, 80, 255), 2)
        # draw work_area
        cv2.rectangle(image_frame, (264, 48), (490, 162), (150, 80, 255), 2)

        final_image = cv2.addWeighted(image_frame, 1.0, black_img, 1.0, 0)
        cv2.imshow('Test Timer', final_image)
        cv2.setMouseCallback('Test Timer', mouse_click)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
