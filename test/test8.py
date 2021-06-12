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
count = 0

# input1 timer
input1_start_time = 0
input1_end_time = 0
input1_total_time = 0
input1_timer_status = -1
input1_is_pass_interested_area = False
input1_counter = 0

# input2 timer
input2_start_time = 0
input2_end_time = 0
input2_total_time = 0
input2_timer_status = -1
input2_is_pass_interested_area = False
input2_counter = 0

# output timer
output_start_time = 0
output_end_time = 0
output_total_time = 0
output_timer_status = -1
output_is_pass_interested_area = False
output_counter = 0

# work timer
work_start_time = 0
work_end_time = 0
work_total_time = 0
work_timer_status = -1
work_counter = 0

# cycle timer
cycle_start_time = 0
cycle_end_time = 0
cycle_timer_status = -1
cycle_total_time = 0
cycle_is_pass_interested_area = False
cycle_counter = 0

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


def my_timer():
    global timer_button
    global current_area_left, current_area_right
    global input1_timer_status, input1_start_time, input1_end_time, input1_total_time, input1_is_pass_interested_area, input1_counter
    global input2_timer_status, input2_start_time, input2_end_time, input2_total_time, input2_is_pass_interested_area, input2_counter
    global output_timer_status, output_start_time, output_end_time, output_total_time, output_is_pass_interested_area, output_counter
    global work_timer_status, work_start_time, work_end_time, work_total_time, work_counter
    global cycle_start_time, cycle_end_time, cycle_timer_status, cycle_total_time, cycle_is_pass_interested_area, cycle_counter

    print(threading.current_thread())

    while True:

        # for this loop can run without lag
        # time.sleep(0)

        # check timer button
        if timer_button is True:
            # timer status = -1 : disable
            # timer status = 0 : standby
            # timer status = 1 : start
            # timer status = 2 : continue record time

            # input1 timer
            # start from work area
            if current_area_left == 4:
                # first time : enable timer
                if input1_timer_status == -1:
                    # set timer to standby
                    input1_timer_status = 0

                elif input1_is_pass_interested_area is True and input1_timer_status == 2:
                    # disable timer and calculate used time
                    input1_timer_status = -1
                    input1_is_pass_interested_area = False
                    # stamp end time
                    input1_end_time = time.time()
                    input1_total_time = round((input1_end_time - input1_start_time), 2)
                    # print('Input1 Time:', input1_total_time, 'seconds')

            # center out of work area and timer is standby
            elif current_area_left == -1 and input1_timer_status == 0:
                # set timer to start
                input1_timer_status = 1
                # stamp start time
                input1_start_time = time.time()

            # once timer start still catch time until timer stop
            elif current_area_left == -1 and input1_timer_status == 1:
                input1_timer_status = 2

            # center is in input1 area once
            if current_area_left == 1:
                input1_is_pass_interested_area = True

            #########################################################

            # input2 timer
            # start from output area
            if current_area_right == 3:
                # first time : enable timer
                if input2_timer_status == -1:
                    # set timer to standby
                    input2_timer_status = 0

            # center out of output area and timer is standby
            elif current_area_right == -1 and input2_timer_status == 0:
                # set timer to start
                input2_timer_status = 1
                # stamp start time
                input2_start_time = time.time()


            # once timer start still catch time until timer stop
            elif current_area_right == -1 and input2_timer_status == 1:
                input2_timer_status = 2

            # center is in input2 area once
            if current_area_right == 2:
                input2_is_pass_interested_area = True

            # center is in work area with timer start and already pass input2 area
            elif current_area_right == 4 and input2_timer_status == 2 and input2_is_pass_interested_area is True:
                # disable timer and calculate used time
                input2_timer_status = -1
                input2_is_pass_interested_area = False
                # stamp end time
                input2_end_time = time.time()
                input2_total_time = round((input2_end_time - input2_start_time), 2)
                # print('Input2 Time:', input2_total_time, 'seconds')

            #########################################################

            # output timer
            # start from work area
            if current_area_right == 4:
                # first time : enable timer
                if output_timer_status == -1:
                    # set timer to standby
                    output_timer_status = 0

            # center out of work area and timer is standby
            elif current_area_right == -1 and output_timer_status == 0:
                # set timer to start
                output_timer_status = 1
                # stamp start time
                output_start_time = time.time()


            # once timer start still catch time until timer stop
            elif current_area_right == -1 and output_timer_status == 1:
                output_timer_status = 2

            # center is in output area once
            if current_area_right == 3:
                output_is_pass_interested_area = True

            # center is out of output area. stop timer and calculate used time
            elif current_area_right == -1 and output_timer_status == 2 and output_is_pass_interested_area is True:
                # disable timer
                output_timer_status = -1
                output_is_pass_interested_area = False
                # stamp end time
                output_end_time = time.time()

                # this case use for fix bug (unknown cause)
                if (output_end_time - output_start_time) == 0:
                    # set timer to standby
                    output_timer_status = 0
                else:
                    output_total_time = round((output_end_time - output_start_time), 2)
                # print('Output Time:', output_total_time, 'seconds')

            #########################################################

            # work timer
            # start from work area
            if current_area_left == 4 and current_area_right == 4:
                # first time : enable timer
                if work_timer_status == -1:
                    # set timer to start
                    work_timer_status = 1
                    # stamp start time
                    work_start_time = time.time()

                # once timer start still catch time until timer stop
                elif work_timer_status == 1:
                    work_timer_status = 2

            # center is out of work area. stop timer and calculate used time
            elif work_timer_status == 2:
                # disable timer
                work_timer_status = -1
                # stamp end time
                work_end_time = time.time()
                work_total_time = round((work_end_time - work_start_time), 2)
                # print('Work Time:', work_total_time, 'seconds')

            #########################################################
            # cycle timer
            # start from output area
            if current_area_right == 3:
                # first time : enable timer
                if cycle_timer_status == -1:
                    # set timer to standby
                    cycle_timer_status = 0

                # center is back to output area with started timer and pass work area
                # stop timer and calculate used time
                elif cycle_timer_status == 2 and cycle_is_pass_interested_area is True:
                    # stamp end time
                    cycle_end_time = time.time()
                    cycle_total_time = round((cycle_end_time - cycle_start_time), 2)

                    # reset timer and pass area
                    cycle_timer_status = -1
                    cycle_is_pass_interested_area = False


            # center out of output with standby timer so it will start timer
            elif current_area_right == -1 and cycle_timer_status == 0:
                # set timer to start
                cycle_timer_status = 1
                # stamp start time
                cycle_start_time = time.time()

            # once timer start still catch time until timer stop
            elif current_area_right == -1 and cycle_timer_status == 1:
                cycle_timer_status = 2

            # center is pass work area
            if current_area_right == 4 and cycle_timer_status == 2:
                cycle_is_pass_interested_area = True

        # display time
        if not input1_total_time < 0:
            if timer_button is False:
                cv2.putText(image_frame, 'Stop', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)
            else:
                cv2.putText(image_frame, str(input1_total_time) + ' seconds', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 2)

        if not input2_total_time < 0:
            if timer_button is False:
                cv2.putText(image_frame, 'Stop', (140, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)
            else:
                cv2.putText(image_frame, str(input2_total_time) + ' seconds', (140, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

        if not output_total_time < 0:
            if timer_button is False:
                cv2.putText(image_frame, 'Stop', (270, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 80, 255), 2)
            else:
                cv2.putText(image_frame, str(output_total_time) + ' seconds', (270, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 80, 255), 2)

        if not work_total_time < 0:
            if timer_button is False:
                cv2.putText(image_frame, 'Stop', (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (150, 80, 255), 2)
            else:
                cv2.putText(image_frame, str(work_total_time) + ' seconds', (400, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (150, 80, 255), 2)

        if not cycle_total_time < 0:
            if timer_button is False:
                cv2.putText(image_frame, 'Stop', (520, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (145, 10, 91), 2)
            else:
                cv2.putText(image_frame, str(cycle_total_time) + ' seconds', (520, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (145, 10, 91), 2)


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

    if is_in_input2_area(center):
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

    if event == cv2.EVENT_MBUTTONDOWN:
        timer_button = False


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(file_name)
    # webcam = cv2.VideoCapture(0)

    # start timer with thread
    thr = threading.Thread(target=my_timer)
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
