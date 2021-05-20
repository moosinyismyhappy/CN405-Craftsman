# Add new tracking method
import cv2
import numpy as np
import math

# Configuration
file_name = '../resources/videos/Full_Working2.mp4'
black_img = cv2.imread('../resources/images/transparent.png')
detect_area = 1000
lower_value = 0.7
upper_value = 1.3
image_frame = None
hsvFrame = None
click_state = 0
boundary_detect_reducer = 15
boundary_extender = 1.2
min_val = 120
input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)
is_learning = True
prev_distance_input1 = -1
curr_distance_input1 = -1
prev_distance_input2 = -1
curr_distance_input2 = -1
prev_distance_output = -1
curr_distance_output = -1
prev_distance_work = -1
curr_distance_work = -1
prev_direction_input1 = -1
curr_direction_input1 = -1
prev_direction_input2 = -1
curr_direction_input2 = -1
prev_direction_output = -1
curr_direction_output = -1
prev_direction_work = -1
curr_direction_work = -1
input1_list = []
input2_list = []
output_list = []
work_list = []
is_input1_ready = 0
is_input2_ready = 0
is_output_ready = 0
is_work_ready = 0
count_approach_input1_left = 0
count_approach_input2_left = 0
count_approach_output_left = 0
count_approach_work_left = 0
count_approach_input1_right = 0
count_approach_input2_right = 0
count_approach_output_right = 0
count_approach_work_right = 0

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
    global input1_position, input2_position, output_position, work_position, click_state

    if click_state == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(black_img, 'input1' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(black_img, (x, y), 2, (0, 0, 255), 2)
            input1_position = x, y
            print('input1 position ', x, y)
            click_state = 1

    elif click_state == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(black_img, 'input2' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 150, 255))
            cv2.circle(black_img, (x, y), 2, (0, 150, 255), 2)
            input2_position = x, y
            print('input2 position ', x, y)
            click_state = 2

    elif click_state == 2:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(black_img, 'output' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 80, 255))
            cv2.circle(black_img, (x, y), 2, (0, 80, 255), 2)
            output_position = x, y
            print('output position ', x, y)
            click_state = 3

    elif click_state == 3:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(black_img, 'working' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (150, 80, 255))
            cv2.circle(black_img, (x, y), 2, (150, 80, 255), 2)
            work_position = x, y
            print('work position ', x, y)
            click_state = 4

    elif click_state == 4:
        # Left Click to get HSV color value from image
        if event == cv2.EVENT_LBUTTONDOWN:
            hsv_lower_left = adjust_lower_hsv(hsvFrame[y, x])
            hsv_upper_left = adjust_upper_hsv(hsvFrame[y, x])

        if event == cv2.EVENT_RBUTTONDOWN:
            hsv_lower_right = adjust_lower_hsv(hsvFrame[y, x])
            hsv_upper_right = adjust_upper_hsv(hsvFrame[y, x])


def get_distance(origin, points):
    return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def find_direction_degree(degree):
    ########################################
    #          250    UP    290            #
    #                                      #
    #      Q2                   Q1         #
    #                                      #
    #   200                        340     #
    #                                      #
    # LEFT          ORIGIN           RIGHT #
    #                                      #
    #   160                        020     #
    #                                      #
    #      Q3                   Q4         #
    #                                      #
    #          110   DOWN   70             #
    ########################################

    if 250 <= degree < 290:
        return 1

    elif 290 <= degree < 340:
        return 2

    elif 340 <= degree < 360:
        return 3

    elif 0 <= degree < 20:
        return 3

    elif 20 <= degree < 70:
        return 5

    elif 70 <= degree < 110:
        return 6

    elif 110 <= degree < 160:
        return 7

    elif 160 <= degree < 200:
        return 8

    elif 200 <= degree < 250:
        return 9


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
            min_y =list[i][1]
        if list[i][1] >= max_y:
            max_y = list[i][1]
    return min_x, max_x, min_y, max_y

def tracking_left(new_center):
    global image_frame, center_bound_left, is_first_detect_left, prev_left, curr_left, is_out_left
    # x,y of center
    x_center, y_center = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = center_bound_left[0], center_bound_left[1], center_bound_left[2], center_bound_left[3]

    if x_center >= x1 and x_center <= x2 and y_center >= y1 and y_center <= y2:
        is_out_left = False
    else:
        point_track_left(x_center, y_center)
        is_out_left = True


def point_track_left(x, y):
    global image_frame, prev_status_left, curr_status_left, curr_left, prev_left
    global input1_position, input2_position, output_position, work_position
    global prev_distance_input1, curr_distance_input1
    global prev_distance_input2, curr_distance_input2
    global prev_distance_output, curr_distance_output
    global prev_distance_work, curr_distance_work
    global prev_direction_input1, curr_direction_input1
    global prev_direction_input2, curr_direction_input2
    global prev_direction_output, curr_direction_output
    global prev_direction_work, curr_direction_work
    global count_approach_input1_left, count_approach_input2_left, count_approach_output_left, count_approach_work_left
    global input1_list, input2_list, output_list, work_list
    global is_input1_ready, is_input2_ready, is_output_ready, is_work_ready

    # Calculate distance to all area
    prev_distance_input1 = curr_distance_input1
    prev_distance_input2 = curr_distance_input2
    prev_distance_output = curr_distance_output
    prev_distance_work = curr_distance_work

    curr_distance_input1 = get_distance(input1_position, (x, y))
    curr_distance_input2 = get_distance(input2_position, (x, y))
    curr_distance_output = get_distance(output_position, (x, y))
    curr_distance_work = get_distance(work_position, (x, y))

    # Calculate direction to all area
    direction_input1_degree = degree(math.atan2(input1_position[1] - y, input1_position[0] - x))
    direction_input2_degree = degree(math.atan2(input2_position[1] - y, input2_position[0] - x))
    direction_output_degree = degree(math.atan2(output_position[1] - y, output_position[0] - x))
    direction_work_degree = degree(math.atan2(work_position[1] - y, work_position[0] - x))

    prev_direction_input1 = curr_direction_input1
    prev_direction_input2 = curr_direction_input2
    prev_direction_output = curr_direction_output
    prev_direction_work = curr_direction_work

    prev_left = curr_left
    curr_left = x, y
    prev_status_left = curr_status_left

    diff_x = curr_left[0] - prev_left[0]
    diff_y = curr_left[1] - prev_left[1]

    point_direction_degree = degree(math.atan2(diff_y, diff_x))

    curr_status_left = find_direction_degree(point_direction_degree)
    curr_direction_input1 = find_direction_degree(direction_input1_degree)
    curr_direction_input2 = find_direction_degree(direction_input2_degree)
    curr_direction_output = find_direction_degree(direction_output_degree)
    curr_direction_work = find_direction_degree(direction_work_degree)

    # increase counter when approach and same direction that area
    if prev_distance_input1 > curr_distance_input1 and curr_direction_input1 == curr_status_left:
        # print('approach input1', prev_direction_input1, curr_direction_input1)
        count_approach_input1_left += 1

    if prev_distance_input2 > curr_distance_input2 and curr_direction_input2 == curr_status_left:
        # print('approach input2', prev_direction_input2, curr_direction_input2)
        count_approach_input2_left += 1

    if prev_distance_output > curr_distance_output and curr_direction_output == curr_status_left:
        # print('approach output', prev_direction_output, curr_direction_output)
        count_approach_output_left += 1

    if prev_distance_work > curr_distance_work and curr_direction_work == curr_status_left:
        # print('approach work', prev_direction_work, curr_direction_work)
        count_approach_work_left += 1

    if curr_status_left != prev_status_left:
        temp = [count_approach_input1_left, count_approach_input2_left, count_approach_output_left,
                count_approach_work_left]
        max_temp = temp.index(max(temp))

        if max_temp == 0:
            if curr_distance_input1 <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 0, 255), 2)
                cv2.putText(black_img, str((x, y, 'input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 0, 255))
                if is_input1_ready == 0:
                    if len(input1_list) < 10:
                        input1_list.append((x, y))
                    else:
                        is_input1_ready = 1
                elif is_input1_ready == 1:
                    print('draw input1 area')
                    average_x, average_y = find_average_point(input1_list)
                    cv2.rectangle(image_frame, (average_x - 50, average_y - 50), (average_x + 50, average_y + 50),
                                  (0, 0, 255), 2)
                    is_input1_ready = -1

        elif max_temp == 1:
            if curr_distance_input2 <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(black_img, str((x, y, 'input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if is_input2_ready == 0:
                    if len(input2_list) < 10:
                        input2_list.append((x, y))
                    else:
                        is_input2_ready = 1
                elif is_input2_ready == 1:
                    average_x, average_y = find_average_point(input2_list)
                    cv2.rectangle(image_frame, (average_x - 50, average_y - 50), (average_x + 50, average_y + 50),
                                  (0, 150, 255), 2)
                    is_input2_ready = -1

        elif max_temp == 2:
            if curr_distance_output <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(black_img, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 80, 255))
                if is_output_ready == 0:
                    if len(output_list) < 10:
                        output_list.append((x, y))
                    else:
                        is_output_ready = 1
                elif is_output_ready == 1:
                    print('draw output area')
                    average_x, average_y = find_average_point(output_list)
                    cv2.rectangle(image_frame, (average_x - 50, average_y - 50), (average_x + 50, average_y + 50),
                                  (0, 80, 255), 2)
                    is_output_ready = -1

        elif max_temp == 3:
            if curr_distance_work <= min_val:
                cv2.circle(black_img, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(black_img, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if is_work_ready == 0:
                    if len(work_list) < 10:
                        work_list.append((x, y))
                    else:
                        is_work_ready = 1
                elif is_work_ready == 1:
                    print('draw work area')
                    average_x, average_y = find_average_point(work_list)
                    cv2.rectangle(image_frame, (average_x - 50, average_y - 50), (average_x + 50, average_y + 50),
                                  (150, 80, 255), 2)
                    is_work_ready = -1

        count_approach_input1_left = 0
        count_approach_input2_left = 0
        count_approach_output_left = 0
        count_approach_work_left = 0


def tracking_right(new_center):
    global image_frame, center_bound_right, is_first_detect_right, prev_right, curr_right, is_out_right
    # x,y of center
    x_center, y_center = new_center[0], new_center[1]

    # x,y of rectangle
    x1, y1, x2, y2 = center_bound_right[0], center_bound_right[1], center_bound_right[2], center_bound_right[3]

    if x_center >= x1 and x_center <= x2 and y_center >= y1 and y_center <= y2:
        is_out_right = False
    else:
        point_track_right(x_center, y_center)
        is_out_right = True


def point_track_right(x, y):
    global image_frame, prev_status_right, curr_status_right, curr_right, prev_right
    global input1_position, input2_position, output_position, work_position
    global prev_distance_input1, curr_distance_input1
    global prev_distance_input2, curr_distance_input2
    global prev_distance_output, curr_distance_output
    global prev_distance_work, curr_distance_work
    global prev_direction_input1, curr_direction_input1
    global prev_direction_input2, curr_direction_input2
    global prev_direction_output, curr_direction_output
    global prev_direction_work, curr_direction_work
    global count_approach_input1_right, count_approach_input2_right, count_approach_output_right, count_approach_work_right
    global input1_list, input2_list, output_list, work_list
    global is_input1_ready, is_input2_ready, is_output_ready, is_work_ready

    # Calculate distance to all area
    prev_distance_input1 = curr_distance_input1
    prev_distance_input2 = curr_distance_input2
    prev_distance_output = curr_distance_output
    prev_distance_work = curr_distance_work

    curr_distance_input1 = get_distance(input1_position, (x, y))
    curr_distance_input2 = get_distance(input2_position, (x, y))
    curr_distance_output = get_distance(output_position, (x, y))
    curr_distance_work = get_distance(work_position, (x, y))

    # Calculate direction to all area
    direction_input1_degree = degree(math.atan2(input1_position[1] - y, input1_position[0] - x))
    direction_input2_degree = degree(math.atan2(input2_position[1] - y, input2_position[0] - x))
    direction_output_degree = degree(math.atan2(output_position[1] - y, output_position[0] - x))
    direction_work_degree = degree(math.atan2(work_position[1] - y, work_position[0] - x))

    prev_direction_input1 = curr_direction_input1
    prev_direction_input2 = curr_direction_input2
    prev_direction_output = curr_direction_output
    prev_direction_work = curr_direction_work

    prev_right = curr_right
    curr_right = x, y
    prev_status_right = curr_status_right

    diff_x = curr_right[0] - prev_right[0]
    diff_y = curr_right[1] - prev_right[1]

    point_direction_degree = degree(math.atan2(diff_y, diff_x))

    curr_status_right = find_direction_degree(point_direction_degree)
    curr_direction_input1 = find_direction_degree(direction_input1_degree)
    curr_direction_input2 = find_direction_degree(direction_input2_degree)
    curr_direction_output = find_direction_degree(direction_output_degree)
    curr_direction_work = find_direction_degree(direction_work_degree)

    # increase counter when approach and same direction that area
    if prev_distance_input1 > curr_distance_input1 and curr_direction_input1 == curr_status_right:
        # print('approach input1', prev_direction_input1, curr_direction_input1)
        count_approach_input1_right += 1

    if prev_distance_input2 > curr_distance_input2 and curr_direction_input2 == curr_status_right:
        # print('approach input2', prev_direction_input2, curr_direction_input2)
        count_approach_input2_right += 1

    if prev_distance_output > curr_distance_output and curr_direction_output == curr_status_right:
        # print('approach output', prev_direction_output, curr_direction_output)
        count_approach_output_right += 1

    if prev_distance_work > curr_distance_work and curr_direction_work == curr_status_right:
        # print('approach work', prev_direction_work, curr_direction_work)
        count_approach_work_right += 1

    if curr_status_right != prev_status_right:
        temp = [count_approach_input1_right, count_approach_input2_right, count_approach_output_right,
                count_approach_work_right]
        max_temp = temp.index(max(temp))

        if max_temp == 0:
            if curr_distance_input1 <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 0, 255), 2)
                cv2.putText(black_img, str((x, y, 'input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 0, 255))
                if is_input1_ready == 0:
                    if len(input1_list) < 10:
                        input1_list.append((x, y))
                    else:
                        is_input1_ready = 1
                elif is_input1_ready == 1:
                    print('draw input1 area')
                    average_x, average_y = find_average_point(input1_list)
                    min_x, max_x, min_y, max_y = find_max_min(input1_list)
                    x1 = int((average_x - (average_x - min_x)) * (1 - boundary_extender))
                    y1 = int((average_y - (average_y - min_y)) * (1 - boundary_extender))
                    x2 = int((average_x + (max_x - average_x)) * boundary_extender)
                    y2 = int((average_y + (max_y - average_y)) * boundary_extender)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (255, 255, 255), 2)
                    is_input1_ready = -1

        elif max_temp == 1:
            if curr_distance_input2 <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(black_img, str((x, y, 'input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if is_input2_ready == 0:
                    if len(input2_list) < 10:
                        input2_list.append((x, y))
                    else:
                        is_input2_ready = 1
                elif is_input2_ready == 1:
                    average_x, average_y = find_average_point(input2_list)
                    min_x, max_x, min_y, max_y = find_max_min(input2_list)
                    x1 = int((average_x - (average_x - min_x)) * (1 - boundary_extender))
                    y1 = int((average_y - (average_y - min_y)) * (1 - boundary_extender))
                    x2 = int((average_x + (max_x - average_x)) * boundary_extender)
                    y2 = int((average_y + (max_y - average_y)) * boundary_extender)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (255, 255, 255), 2)
                    is_input2_ready = -1

        elif max_temp == 2:
            if curr_distance_output <= min_val:
                cv2.circle(black_img, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(black_img, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 80, 255))
                if is_output_ready == 0:
                    if len(output_list) < 10:
                        output_list.append((x, y))
                    else:
                        is_output_ready = 1
                elif is_output_ready == 1:
                    print('draw output area')
                    average_x, average_y = find_average_point(output_list)
                    min_x, max_x, min_y, max_y = find_max_min(output_list)
                    x1 = int((average_x - (average_x - min_x)) * (1 - boundary_extender))
                    y1 = int((average_y - (average_y - min_y)) * (1 - boundary_extender))
                    x2 = int((average_x + (max_x - average_x)) * boundary_extender)
                    y2 = int((average_y + (max_y - average_y)) * boundary_extender)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (255, 255, 255), 2)
                    is_output_ready = -1

        elif max_temp == 3:
            if curr_distance_work <= min_val:
                cv2.circle(black_img, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(black_img, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if is_work_ready == 0:
                    if len(work_list) < 20:
                        work_list.append((x, y))
                    else:
                        is_work_ready = 1
                elif is_work_ready == 1:
                    print('draw work area')
                    average_x, average_y = find_average_point(work_list)
                    min_x, max_x, min_y, max_y = find_max_min(work_list)
                    x1 = int((average_x - (average_x - min_x))*(1-boundary_extender))
                    y1 = int((average_y - (average_y - min_y))*(1-boundary_extender))
                    x2 = int((average_x + (max_x - average_x))*boundary_extender)
                    y2 = int((average_y + (max_y - average_y))*boundary_extender)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (255, 255, 255), 2)
                    is_work_ready = -1

        count_approach_input1_right = 0
        count_approach_input2_right = 0
        count_approach_output_right = 0
        count_approach_work_right = 0


if __name__ == "__main__":

    # Capturing video through webcam
    webcam = cv2.VideoCapture(file_name)
    # webcam = cv2.VideoCapture(1)
    while True:
        # Receive stream image from camera
        _, image_frame = webcam.read()
        image_frame = cv2.resize(image_frame, (640, 480))
        # image_frame = cv2.flip(image_frame, 1)

        # Change color space from RGB to HSV
        hsvFrame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

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

                # step one : draw static rectangle over first detect area
                if is_first_detect_left == 0:
                    center_bound_left[0] = x + boundary_detect_reducer
                    center_bound_left[1] = y + boundary_detect_reducer
                    center_bound_left[2] = x + w - boundary_detect_reducer
                    center_bound_left[3] = y + h - boundary_detect_reducer
                    curr_left = center
                    prev_left = center
                    prev_status_left = -1
                    curr_status_left = -1
                    is_first_detect_left = 1
                elif is_first_detect_left == 1:
                    tracking_left(center)
                    if is_out_left:
                        center_bound_left[0] = x + boundary_detect_reducer
                        center_bound_left[1] = y + boundary_detect_reducer
                        center_bound_left[2] = x + w - boundary_detect_reducer
                        center_bound_left[3] = y + h - boundary_detect_reducer

                image_frame = cv2.rectangle(image_frame, (center_bound_left[0], center_bound_left[1]),
                                            (center_bound_left[2], center_bound_left[3]),
                                            (180, 180, 180), 2)
                image_frame = cv2.circle(image_frame, center, 2, (0, 0, 255), 2)
                cv2.putText(image_frame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (180, 180, 180))
                image_frame = cv2.rectangle(image_frame, (x, y),
                                            (x + w, y + h),
                                            (0, 0, 255), 2)

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

                # step one : draw static rectangle over first detect area
                if is_first_detect_right == 0:
                    center_bound_right[0] = x + boundary_detect_reducer
                    center_bound_right[1] = y + boundary_detect_reducer
                    center_bound_right[2] = x + w - boundary_detect_reducer
                    center_bound_right[3] = y + h - boundary_detect_reducer
                    curr_right = center
                    prev_right = center
                    prev_status_right = -1
                    curr_status_right = -1
                    is_first_detect_right = 1
                elif is_first_detect_right == 1:
                    tracking_right(center)
                    if is_out_right:
                        center_bound_right[0] = x + boundary_detect_reducer
                        center_bound_right[1] = y + boundary_detect_reducer
                        center_bound_right[2] = x + w - boundary_detect_reducer
                        center_bound_right[3] = y + h - boundary_detect_reducer

                image_frame = cv2.rectangle(image_frame, (center_bound_right[0], center_bound_right[1]),
                                            (center_bound_right[2], center_bound_right[3]),
                                            (180, 180, 180), 2)
                image_frame = cv2.circle(image_frame, center, 2, (0, 0, 255), 2)
                cv2.putText(image_frame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (180, 180, 180))
                image_frame = cv2.rectangle(image_frame, (x, y),
                                            (x + w, y + h),
                                            (0, 255, 255), 2)

        if is_input1_ready == -1:
            average_x, average_y = find_average_point(input1_list)
            min_x, max_x, min_y, max_y = find_max_min(input1_list)
            x1 = average_x - (average_x - min_x)
            y1 = average_y - (average_y - min_y)
            x2 = average_x + (max_x - average_x)
            y2 = average_y + (max_y - average_y)
            cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                          (0, 0, 255), 2)
        if is_input2_ready == -1:
            average_x, average_y = find_average_point(input2_list)
            min_x, max_x, min_y, max_y = find_max_min(input2_list)
            x1 = average_x - (average_x - min_x)
            y1 = average_y - (average_y - min_y)
            x2 = average_x + (max_x - average_x)
            y2 = average_y + (max_y - average_y)
            cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                          (0, 150, 255), 2)
        if is_output_ready == -1:
            average_x, average_y = find_average_point(output_list)
            min_x, max_x, min_y, max_y = find_max_min(output_list)
            x1 = average_x - (average_x - min_x)
            y1 = average_y - (average_y - min_y)
            x2 = average_x + (max_x - average_x)
            y2 = average_y + (max_y - average_y)
            cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                          (0, 80, 255), 2)
        if is_work_ready == -1:
            average_x, average_y = find_average_point(work_list)
            min_x, max_x, min_y, max_y = find_max_min(work_list)
            x1 = average_x - (average_x - min_x)
            y1 = average_y - (average_y - min_y)
            x2 = average_x + (max_x - average_x)
            y2 = average_y + (max_y - average_y)
            cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                          (150, 80, 255), 2)

        final_image = cv2.addWeighted(image_frame, 1.0, black_img, 1.0, 0)
        cv2.imshow("Multiple color Detection", final_image)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
