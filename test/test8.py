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
current_area_left = -1
current_area_right = -1
timer_button = False

# input1 timer
input1_start_time = 0
input1_end_time = 0
input1_timer_status = -1
input1_is_from_input1_area = False

# input2 timer
input2_start_time = 0
input2_end_time = 0
input2_timer_status = -1
input2_is_from_work_area = False

# output timer
output_start_time = 0
output_end_time = 0
output_timer_status = -1
output_is_in_output_area = False

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
    global current_area_left
    global input1_timer_status, input1_start_time, input1_end_time, input1_is_from_input1_area
    global input2_timer_status, input2_start_time, input2_end_time, input2_is_from_work_area
    global output_timer_status, output_start_time, output_end_time, output_is_in_output_area

    print(threading.current_thread())

    while True:

        # for this loop can run without lag
        time.sleep(0)

        # check timer button
        if timer_button is True:

            # input1 timer
            # start from work area
            if current_area_left == 4:
                if input1_is_from_input1_area is False:
                    input1_timer_status = 0
                # end at work area
                elif input1_timer_status == 1:
                    input1_end_time = time.time()
                    print('Input1 Time :', round((input1_end_time - input1_start_time), 2), 'seconds')
                    input1_timer_status = 0

            # center out of work area
            else:
                # set timer to start
                if input1_timer_status == 0:
                    input1_start_time = time.time()
                    input1_timer_status = 1
                    input1_is_from_input1_area = True

            #######################################################

            """# input2 timer
            # start from output area
            if current_area_right == 3:
                input2_timer_status = 0
                input2_is_from_work_area = True

            # do when center out of output area
            else:
                # check center came from work area or not
                if input2_is_from_work_area is True:
                    # set timer to start
                    if input2_timer_status == 0:
                        input2_start_time = time.time()
                        input2_timer_status = 1

                # end at work area
                if current_area_right == 4 and input2_timer_status == 1:
                    input2_end_time = time.time()
                    print('Input2 Time :', round((input2_end_time - input2_start_time), 2), 'seconds')
                    input2_timer_status = 0
                    input2_is_from_work_area = False"""

            #######################################################

            # output timer
            # start from work area
            if current_area_right == 4:
                output_timer_status = 0

            # do when center out of work area
            else:
                # set timer to start
                if output_timer_status == 0:
                    print('start timer output')
                    output_timer_status = 1

                elif output_timer_status == 1:
                    pass

                if current_area_right == 3:
                    output_is_in_output_area = True
                else:
                    output_is_in_output_area = False


def where_is_center_in_area_left(center):
    global current_area_left

    x_text = center[0] - 15
    y_text = center[1] - 15

    if is_in_input1_area(center):
        cv2.putText(image_frame, 'In input1', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_left = 1


    elif is_in_input2_area(center):
        cv2.putText(image_frame, 'In input2', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_left = 2


    elif is_in_output_area(center):
        cv2.putText(image_frame, 'In output', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_left = 3


    elif is_in_work_area(center):
        cv2.putText(image_frame, 'In work', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_left = 4

    else:
        current_area_left = -1


def where_is_center_in_area_right(center):
    global current_area_right

    x_text = center[0] - 15
    y_text = center[1] - 15

    if is_in_input1_area(center):
        cv2.putText(image_frame, 'In input1', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_right = 1


    elif is_in_input2_area(center):
        cv2.putText(image_frame, 'In input2', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_right = 2


    elif is_in_output_area(center):
        cv2.putText(image_frame, 'In output', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_right = 3


    elif is_in_work_area(center):
        cv2.putText(image_frame, 'In work', (x_text, y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        current_area_right = 4

    else:
        current_area_right = -1


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
        timer_button = True


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

                # find where area that center at
                where_is_center_in_area_right(center)

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
