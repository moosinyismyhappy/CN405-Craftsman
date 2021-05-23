# new method for auto detect area (color)

import cv2
import numpy as np
import math

# load image file and video
file_name = '../resources/videos/Full_Working1.mp4'
background_image = cv2.imread('../resources/images/transparent.png')
image_frame = None
hsv_frame = None
detect_area = 1000
lower_range = 0.7
upper_range = 1.3
click_counter = 0
boundary_detect_reducer = 10

calibrate_area_status = True
minimum_distance = 120
rectangle_extender = 10

input1_calibrate_time = 8
input2_calibrate_time = 8
output_calibrate_time = 8
work_calibrate_time = 8

input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)

input1_list = []
input2_list = []
output_list = []
work_list = []

input1_calibrate_status = 0
input2_calibrate_status = 0
output_calibrate_status = 0
work_calibrate_status = 0

input1_calibrate_area = [-1, -1, -1, -1]
input2_calibrate_area = [-1, -1, -1, -1]
output_calibrate_area = [-1, -1, -1, -1]
work_calibrate_area = [-1, -1, -1, -1]

display_input1_area = False
display_input2_area = False
display_output_area = False
display_work_area = False

# For left hand
hsv_lower_left = [-1, -1, -1]
hsv_upper_left = [-1, -1, -1]
boundary_left = [-1, -1, -1, -1]
is_out_bound_left = False
is_first_detect_left = 0

prev_position_left = -1
curr_position_left = -1

prev_direction_left = -1
curr_direction_left = -1

prev_distance_input1_left = -1
curr_distance_input1_left = -1

prev_distance_input2_left = -1
curr_distance_input2_left = -1

prev_distance_output_left = -1
curr_distance_output_left = -1

prev_distance_work_left = -1
curr_distance_work_left = -1

prev_direction_input1_left = -1
curr_direction_input1_left = -1

prev_direction_input2_left = -1
curr_direction_input2_left = -1

prev_direction_output_left = -1
curr_direction_output_left = -1

prev_direction_work_left = -1
curr_direction_work_left = -1

count_approaching_input1_left = 0
count_approaching_input2_left = 0
count_approaching_output_left = 0
count_approaching_work_left = 0

# For right hand
hsv_lower_right = [-1, -1, -1]
hsv_upper_right = [-1, -1, -1]
boundary_right = [-1, -1, -1, -1]
is_out_bound_right = False
is_first_detect_right = 0

prev_position_right = -1
curr_position_right = -1

prev_direction_right = -1
curr_direction_right = -1

prev_distance_input1_right = -1
curr_distance_input1_right = -1

prev_distance_input2_right = -1
curr_distance_input2_right = -1

prev_distance_output_right = -1
curr_distance_output_right = -1

prev_distance_work_right = -1
curr_distance_work_right = -1

prev_direction_input1_right = -1
curr_direction_input1_right = -1

prev_direction_input2_right = -1
curr_direction_input2_right = -1

prev_direction_output_right = -1
curr_direction_output_right = -1

prev_direction_work_right = -1
curr_direction_work_right = -1

count_approaching_input1_right = 0
count_approaching_input2_right = 0
count_approaching_output_right = 0
count_approaching_work_right = 0


def adjust_max_hsv(input_val):
    if (input_val > 255):
        input_val = 255
    return input_val


def adjust_lower_hsv(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(int(i * lower_range))
    return temp_list


def adjust_upper_hsv(input_list):
    temp_list = []
    for i in input_list:
        temp_list.append(int(adjust_max_hsv(i * upper_range)))
    return temp_list


def calculate_distance(origin, points):
    return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))


def calculate_degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def find_direction_number(degree):
    ########################################
    #          260    UP    280            #
    #                                      #
    #      Q2                   Q1         #
    #                                      #
    #   190                        350     #
    #                                      #
    # LEFT          ORIGIN           RIGHT #
    #                                      #
    #   170                        010     #
    #                                      #
    #      Q3                   Q4         #
    #                                      #
    #          100   DOWN   80             #
    ########################################
    if 260 <= degree < 280:
        return 1
    elif 280 <= degree < 350:
        return 2
    elif 350 <= degree < 360:
        return 3
    elif 0 <= degree < 10:
        return 3
    elif 10 <= degree < 80:
        return 4
    elif 80 <= degree < 100:
        return 5
    elif 100 <= degree < 170:
        return 6
    elif 170 <= degree < 190:
        return 7
    elif 190 <= degree < 260:
        return 8


def find_average_point(list):
    sum_x = 0
    sum_y = 0
    for i in list:
        sum_x += i[0]
        sum_y += i[1]
    average_x = int(sum_x / len(list))
    average_y = int(sum_y / len(list))
    return average_x, average_y


def find_max_min(list):
    min_x = list[0][0]
    min_y = list[0][1]
    max_x = list[0][0]
    max_y = list[0][1]
    for i in range(len(list)):
        if list[i][0] <= min_x:
            min_x = list[i][0]
        if list[i][0] >= max_x:
            max_x = list[i][0]
        if list[i][1] <= min_y:
            min_y = list[i][1]
        if list[i][1] >= max_y:
            max_y = list[i][1]
    return min_x, max_x, min_y, max_y


def process_rectangle(list):
    global rectangle_extender
    min_x, max_x, min_y, max_y = find_max_min(list)
    min_x -= rectangle_extender
    min_y -= rectangle_extender
    max_x += rectangle_extender
    max_y += rectangle_extender
    return min_x, min_y, max_x, max_y


def mouse_click(event, x, y, flags, param):
    global click_counter, background_image
    global hsv_lower_left, hsv_upper_left, hsv_lower_right, hsv_upper_right
    global input1_position, input2_position, output_position, work_position

    if click_counter == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(background_image, 'Input1' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(background_image, (x, y), 2, (0, 0, 255), 2)
            input1_position = x, y
            click_counter = 1

    elif click_counter == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(background_image, 'Input2' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 150, 255))
            cv2.circle(background_image, (x, y), 2, (0, 150, 255), 2)
            input2_position = x, y
            click_counter = 2

    elif click_counter == 2:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(background_image, 'Output' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 80, 255))
            cv2.circle(background_image, (x, y), 2, (0, 80, 255), 2)
            output_position = x, y
            click_counter = 3

    elif click_counter == 3:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(background_image, 'Working' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (150, 80, 255))
            cv2.circle(background_image, (x, y), 2, (150, 80, 255), 2)
            work_position = x, y
            click_counter = 4

    elif click_counter == 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_lower_left = adjust_lower_hsv(hsv_frame[y, x])
            hsv_upper_left = adjust_upper_hsv(hsv_frame[y, x])

        if event == cv2.EVENT_RBUTTONDOWN:
            hsv_lower_right = adjust_lower_hsv(hsv_frame[y, x])
            hsv_upper_right = adjust_upper_hsv(hsv_frame[y, x])


def tracking_left(new_center):
    global is_out_bound_left, boundary_left

    # x,y of center
    x_center, y_center = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = boundary_left[0], boundary_left[1], boundary_left[2], boundary_left[3]

    if x_center >= x1 and x_center <= x2 and y_center >= y1 and y_center <= y2:
        is_out_bound_left = False
    else:
        point_track_left(x_center, y_center)
        is_out_bound_left = True


def point_track_left(x, y):
    global image_frame, minimum_distance, calibrate_area_status, rectangle_extender
    global input1_calibrate_time, input2_calibrate_time, output_calibrate_time, work_calibrate_time
    global input1_position, input2_position, output_position, work_position
    global prev_position_left, curr_position_left, prev_direction_left, curr_direction_left
    global prev_distance_input1_left, curr_distance_input1_left, prev_direction_input1_left, curr_direction_input1_left
    global prev_distance_input2_left, curr_distance_input2_left, prev_direction_input2_left, curr_direction_input2_left
    global prev_distance_output_left, curr_distance_output_left, prev_direction_output_left, curr_direction_output_left
    global prev_distance_work_left, curr_distance_work_left, prev_direction_work_left, curr_direction_work_left
    global count_approaching_input1_left, count_approaching_input2_left, count_approaching_output_left, count_approaching_work_left
    global input1_list, input2_list, output_list, work_list
    global input1_calibrate_status, input2_calibrate_status, output_calibrate_status, work_calibrate_status
    global display_input1_area, display_input2_area, display_output_area, display_work_area
    global input1_calibrate_area, input2_calibrate_area, output_calibrate_area, work_calibrate_area

    # set current point position and direction to previous
    prev_direction_left = curr_direction_left
    prev_position_left = curr_position_left
    curr_position_left = x, y

    # calculate difference between current point and previous point
    diff_x = curr_position_left[0] - prev_position_left[0]
    diff_y = curr_position_left[1] - prev_position_left[1]

    # set current distance to previous
    prev_distance_input1_left = curr_distance_input1_left
    prev_distance_input2_left = curr_distance_input2_left
    prev_distance_output_left = curr_distance_output_left
    prev_distance_work_left = curr_distance_work_left

    # set current direction to previous
    prev_direction_input1_left = curr_direction_input1_left
    prev_direction_input2_left = curr_direction_input2_left
    prev_direction_output_left = curr_direction_output_left
    prev_direction_work_left = curr_direction_work_left

    # temp variable
    # Calculate direction from previous to current point
    point_direction_degree = calculate_degree(math.atan2(diff_y, diff_x))

    # temp variable
    # Calculate direction from current point to all area
    direction_input1_degree = calculate_degree(math.atan2(input1_position[1] - y, input1_position[0] - x))
    direction_input2_degree = calculate_degree(math.atan2(input2_position[1] - y, input2_position[0] - x))
    direction_output_degree = calculate_degree(math.atan2(output_position[1] - y, output_position[0] - x))
    direction_work_degree = calculate_degree(math.atan2(work_position[1] - y, work_position[0] - x))

    # Calculate distance from current point to all area
    curr_distance_input1_left = calculate_distance(input1_position, (x, y))
    curr_distance_input2_left = calculate_distance(input2_position, (x, y))
    curr_distance_output_left = calculate_distance(output_position, (x, y))
    curr_distance_work_left = calculate_distance(work_position, (x, y))

    # find direction number
    curr_direction_left = find_direction_number(point_direction_degree)
    curr_direction_input1_left = find_direction_number(direction_input1_degree)
    curr_direction_input2_left = find_direction_number(direction_input2_degree)
    curr_direction_output_left = find_direction_number(direction_output_degree)
    curr_direction_work_left = find_direction_number(direction_work_degree)

    # increase counter when approaching area with lower distance and not change direction
    # except work area due to many direction to approaching. it's use only distance
    if prev_distance_input1_left > curr_distance_input1_left and curr_direction_input1_left == curr_direction_left:
        count_approaching_input1_left += 1

    if prev_distance_input2_left > curr_distance_input2_left and curr_direction_input2_left == curr_direction_left:
        count_approaching_input2_left += 1

    if prev_distance_output_left > curr_distance_output_left and curr_direction_output_left == curr_direction_left:
        count_approaching_output_left += 1

    if prev_distance_work_left > curr_distance_work_left:
        count_approaching_work_left += 1

    # do this when direction is changed
    if curr_direction_left != prev_direction_left:

        # temp variable
        # create temp list to keep counter and find index that has maximum counter that mean maximum approach
        max_approaching_list = [count_approaching_input1_left, count_approaching_input2_left,
                                count_approaching_output_left,
                                count_approaching_work_left]
        max_approaching = max_approaching_list.index(max(max_approaching_list))

        # approached input1
        if max_approaching == 0:
            if curr_distance_input1_left <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 0, 255), 2)
                cv2.putText(background_image, str((x, y, 'Input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 0, 255))
                if calibrate_area_status:
                    if input1_calibrate_status == 0:
                        input1_list.append((x, y))

        # approached input2
        elif max_approaching == 1:
            if curr_distance_input2_left <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(background_image, str((x, y, 'Input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if calibrate_area_status:
                    if input2_calibrate_status == 0:
                        input2_list.append((x, y))

        # approached output
        elif max_approaching == 2:
            if curr_distance_output_left <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(background_image, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 80, 255))
                if calibrate_area_status:
                    if output_calibrate_status == 0:
                        output_list.append((x, y))

        # approached work
        elif max_approaching == 3:
            if curr_distance_work_left <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(background_image, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if calibrate_area_status:
                    if work_calibrate_status == 0:
                        work_list.append((x, y))

        # reset approach counter after change direction
        count_approaching_input1_left = count_approaching_input2_left = count_approaching_output_left = count_approaching_work_left = 0

    if len(input1_list) == input1_calibrate_time:
        x1, y1, x2, y2 = process_rectangle(input1_list)
        input1_calibrate_area = [x1,y1,x2,y2]
        # stop calibrate and clear list
        input1_calibrate_status = 1
        # enable display area
        display_input1_area = True

    if len(input2_list) == input2_calibrate_time:
        x1, y1, x2, y2 = process_rectangle(input2_list)
        input2_calibrate_area = [x1, y1, x2, y2]
        # stop calibrate and clear list
        input2_calibrate_status = 1
        # enable display area
        display_input2_area = True

    if len(output_list) == output_calibrate_time:
        x1, y1, x2, y2 = process_rectangle(output_list)
        output_calibrate_area = [x1, y1, x2, y2]
        # stop calibrate and clear list
        output_calibrate_status = 1
        # enable display area
        display_output_area = True

    if len(work_list) == work_calibrate_time:
        x1, y1, x2, y2 = process_rectangle(work_list)
        work_calibrate_area = [x1, y1, x2, y2]
        # stop calibrate and clear list
        work_calibrate_status = 1
        # enable display area
        display_work_area = True

    # check if all area is finished calibrate set calibrate status to False and reset each area to prepare new calibrate
    if input1_calibrate_status == input2_calibrate_status == output_calibrate_status == work_calibrate_status == 1:
        input1_calibrate_status = input2_calibrate_status = output_calibrate_status = work_calibrate_status = 0
        calibrate_area_status = False
        print('all area has been drawn')


def tracking_right(new_center):
    global boundary_right, is_out_bound_right
    # x,y of center
    x_center, y_center = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = boundary_right[0], boundary_right[1], boundary_right[2], boundary_right[3]

    if x1 <= x_center <= x2 and y1 <= y_center <= y2:
        is_out_bound_right = False
    else:
        point_track_right(x_center, y_center)
        is_out_bound_right = True


def point_track_right(x, y):
    global image_frame, minimum_distance, calibrate_area_status, rectangle_extender
    global input1_calibrate_time, input2_calibrate_time, output_calibrate_time, work_calibrate_time
    global input1_position, input2_position, output_position, work_position
    global prev_position_right, curr_position_right, prev_direction_right, curr_direction_right
    global prev_distance_input1_right, curr_distance_input1_right, prev_direction_input1_right, curr_direction_input1_right
    global prev_distance_input2_right, curr_distance_input2_right, prev_direction_input2_right, curr_direction_input2_right
    global prev_distance_output_right, curr_distance_output_right, prev_direction_output_right, curr_direction_output_right
    global prev_distance_work_right, curr_distance_work_right, prev_direction_work_right, curr_direction_work_right
    global count_approaching_input1_right, count_approaching_input2_right, count_approaching_output_right, count_approaching_work_right
    global input1_list, input2_list, output_list, work_list
    global input1_calibrate_status, input2_calibrate_status, output_calibrate_status, work_calibrate_status
    global display_input1_area, display_input2_area, display_output_area, display_work_area
    global input1_calibrate_area, input2_calibrate_area, output_calibrate_area, work_calibrate_area

    # set current point position and direction to previous
    prev_direction_right = curr_direction_right
    prev_position_right = curr_position_right
    curr_position_right = x, y

    # calculate difference between current point and previous point
    diff_x = curr_position_right[0] - prev_position_right[0]
    diff_y = curr_position_right[1] - prev_position_right[1]

    # set current distance to previous
    prev_distance_input1_right = curr_distance_input1_right
    prev_distance_input2_right = curr_distance_input2_right
    prev_distance_output_right = curr_distance_output_right
    prev_distance_work_right = curr_distance_work_right

    # set current direction to previous
    prev_direction_input1_right = curr_direction_input1_right
    prev_direction_input2_right = curr_direction_input2_right
    prev_direction_output_right = curr_direction_output_right
    prev_direction_work_right = curr_direction_work_right

    # temp variable
    # Calculate direction from previous to current point
    point_direction_degree = calculate_degree(math.atan2(diff_y, diff_x))

    # temp variable
    # Calculate direction from current point to all area
    direction_input1_degree = calculate_degree(math.atan2(input1_position[1] - y, input1_position[0] - x))
    direction_input2_degree = calculate_degree(math.atan2(input2_position[1] - y, input2_position[0] - x))
    direction_output_degree = calculate_degree(math.atan2(output_position[1] - y, output_position[0] - x))
    direction_work_degree = calculate_degree(math.atan2(work_position[1] - y, work_position[0] - x))

    # Calculate distance from current point to all area
    curr_distance_input1_right = calculate_distance(input1_position, (x, y))
    curr_distance_input2_right = calculate_distance(input2_position, (x, y))
    curr_distance_output_right = calculate_distance(output_position, (x, y))
    curr_distance_work_right = calculate_distance(work_position, (x, y))

    # find direction number
    curr_direction_right = find_direction_number(point_direction_degree)
    curr_direction_input1_right = find_direction_number(direction_input1_degree)
    curr_direction_input2_right = find_direction_number(direction_input2_degree)
    curr_direction_output_right = find_direction_number(direction_output_degree)
    curr_direction_work_right = find_direction_number(direction_work_degree)

    # increase counter when approaching area with lower distance and not change direction
    # except work area due to many direction to approaching. it's use only distance
    if prev_distance_input1_right > curr_distance_input1_right and curr_direction_input1_right == curr_direction_right:
        count_approaching_input1_right += 1

    if prev_distance_input2_right > curr_distance_input2_right and curr_direction_input2_right == curr_direction_right:
        count_approaching_input2_right += 1

    if prev_distance_output_right > curr_distance_output_right and curr_direction_output_right == curr_direction_right:
        count_approaching_output_right += 1

    if prev_distance_work_right > curr_distance_work_right:
        count_approaching_work_right += 1

    # do this when direction is changed
    if curr_direction_right != prev_direction_right:

        # temp variable
        # create temp list to keep counter and find index that has maximum counter that mean maximum approach
        max_approaching_list = [count_approaching_input1_right, count_approaching_input2_right,
                                count_approaching_output_right,
                                count_approaching_work_right]
        max_approaching = max_approaching_list.index(max(max_approaching_list))

        # approached input1
        if max_approaching == 0:
            if curr_distance_input1_right <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 0, 255), 2)
                cv2.putText(background_image, str((x, y, 'Input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 0, 255))
                if calibrate_area_status:
                    if input1_calibrate_status == 0:
                        input1_list.append((x, y))

        # approached input2
        elif max_approaching == 1:
            if curr_distance_input2_right <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(background_image, str((x, y, 'Input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if calibrate_area_status:
                    if input2_calibrate_status == 0:
                        input2_list.append((x, y))

        # approached output
        elif max_approaching == 2:
            if curr_distance_output_right <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(background_image, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 80, 255))
                if calibrate_area_status:
                    if output_calibrate_status == 0:
                        output_list.append((x, y))

        # approached work
        elif max_approaching == 3:
            if curr_distance_work_right <= minimum_distance:
                cv2.circle(background_image, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(background_image, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if calibrate_area_status:
                    if work_calibrate_status == 0:
                        work_list.append((x, y))

        # reset approach counter after change direction
        count_approaching_input1_right = count_approaching_input2_right = count_approaching_output_right = count_approaching_work_right = 0

        if len(input1_list) == input1_calibrate_time:
            x1, y1, x2, y2 = process_rectangle(input1_list)
            input1_calibrate_area = [x1, y1, x2, y2]
            # stop calibrate and clear list
            input1_calibrate_status = 1
            # enable display area
            display_input1_area = True

        if len(input2_list) == input2_calibrate_time:
            x1, y1, x2, y2 = process_rectangle(input2_list)
            input2_calibrate_area = [x1, y1, x2, y2]
            # stop calibrate and clear list
            input2_calibrate_status = 1
            # enable display area
            display_input2_area = True

        if len(output_list) == output_calibrate_time:
            x1, y1, x2, y2 = process_rectangle(output_list)
            output_calibrate_area = [x1, y1, x2, y2]
            # stop calibrate and clear list
            output_calibrate_status = 1
            # enable display area
            display_output_area = True

        if len(work_list) == work_calibrate_time:
            x1, y1, x2, y2 = process_rectangle(work_list)
            work_calibrate_area = [x1, y1, x2, y2]
            # stop calibrate and clear list
            work_calibrate_status = 1
            # enable display area
            display_work_area = True

        # if all area is finished calibrate set calibrate status to False and reset each area to prepare new calibrate
        if input1_calibrate_status == input2_calibrate_status == output_calibrate_status == work_calibrate_status == 1:
            input1_calibrate_status = input2_calibrate_status = output_calibrate_status = work_calibrate_status = 0
            calibrate_area_status = False
            print('all area has been drawn')

if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(file_name)
    # webcam = cv2.VideoCapture(1)
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

                # draw static rectangle over first detect area
                if is_first_detect_left == 0:
                    boundary_left[0] = x + boundary_detect_reducer
                    boundary_left[1] = y + boundary_detect_reducer
                    boundary_left[2] = x + w - boundary_detect_reducer
                    boundary_left[3] = y + h - boundary_detect_reducer
                    curr_position_left = center
                    prev_position_left = center
                    prev_direction_left = -1
                    curr_direction_left = -1
                    is_first_detect_left = 1
                elif is_first_detect_left == 1:
                    tracking_left(center)
                    if is_out_bound_left:
                        boundary_left[0] = x + boundary_detect_reducer
                        boundary_left[1] = y + boundary_detect_reducer
                        boundary_left[2] = x + w - boundary_detect_reducer
                        boundary_left[3] = y + h - boundary_detect_reducer

                image_frame = cv2.rectangle(image_frame, (boundary_left[0], boundary_left[1]),
                                            (boundary_left[2], boundary_left[3]),
                                            (180, 180, 180), 2)
                image_frame = cv2.circle(image_frame, center, 2, (0, 0, 255), 2)
                cv2.putText(image_frame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (180, 180, 180))
                image_frame = cv2.rectangle(image_frame, (x, y),
                                            (x + w, y + h),
                                            (0, 0, 255), 2)

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

                # draw static rectangle over first detect area
                if is_first_detect_right == 0:
                    boundary_right[0] = x + boundary_detect_reducer
                    boundary_right[1] = y + boundary_detect_reducer
                    boundary_right[2] = x + w - boundary_detect_reducer
                    boundary_right[3] = y + h - boundary_detect_reducer
                    curr_position_right = center
                    prev_position_right = center
                    prev_direction_right = -1
                    curr_direction_right = -1
                    is_first_detect_right = 1
                elif is_first_detect_right == 1:
                    tracking_right(center)
                    if is_out_bound_right:
                        boundary_right[0] = x + boundary_detect_reducer
                        boundary_right[1] = y + boundary_detect_reducer
                        boundary_right[2] = x + w - boundary_detect_reducer
                        boundary_right[3] = y + h - boundary_detect_reducer

                image_frame = cv2.rectangle(image_frame, (boundary_right[0], boundary_right[1]),
                                            (boundary_right[2], boundary_right[3]),
                                            (180, 180, 180), 2)
                image_frame = cv2.circle(image_frame, center, 2, (0, 0, 255), 2)
                cv2.putText(image_frame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (180, 180, 180))
                image_frame = cv2.rectangle(image_frame, (x, y),
                                            (x + w, y + h),
                                            (0, 255, 255), 2)

        if display_input1_area:
            x1 = input1_calibrate_area[0]
            y1 = input1_calibrate_area[1]
            x2 = input1_calibrate_area[2]
            y2 = input1_calibrate_area[3]
            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        if display_input2_area:
            x1 = input2_calibrate_area[0]
            y1 = input2_calibrate_area[1]
            x2 = input2_calibrate_area[2]
            y2 = input2_calibrate_area[3]
            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)

        if display_output_area:
            x1 = output_calibrate_area[0]
            y1 = output_calibrate_area[1]
            x2 = output_calibrate_area[2]
            y2 = output_calibrate_area[3]
            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 80, 255), 2)

        if display_work_area:
            x1 = work_calibrate_area[0]
            y1 = work_calibrate_area[1]
            x2 = work_calibrate_area[2]
            y2 = work_calibrate_area[3]
            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (150, 80, 255), 2)

        final_image = cv2.addWeighted(image_frame, 1.0, background_image, 1.0, 0)
        cv2.imshow('Multiple color Detection', final_image)
        cv2.setMouseCallback('Multiple color Detection', mouse_click)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
