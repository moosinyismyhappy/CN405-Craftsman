# new method for auto detect area (Mouse)

import cv2
import math

# load image file
image_frame = cv2.imread('../resources/images/black_background.png')

boundary = [-1, -1, -1, -1]
click_counter = 0
calibrate_area_status = True
minimum_distance = 120
rectangle_extender = 10

input1_calibrate_time = 5
input2_calibrate_time = 5
output_calibrate_time = 5
work_calibrate_time = 5

input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)

input1_list = []
input2_list = []
output_list = []
work_list = []

count_approaching_input1 = 0
count_approaching_input2 = 0
count_approaching_output = 0
count_approaching_work = 0

input1_calibrate_status = 0
input2_calibrate_status = 0
output_calibrate_status = 0
work_calibrate_status = 0

# previous and current of distance and direction
prev_position = -1
curr_position = -1

prev_direction = -1
curr_direction = -1

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


def mouse_click(event, x, y, flags, param):
    global image_frame, click_counter, boundary
    global input1_position, input2_position, output_position, work_position
    global prev_position, curr_position
    global prev_distance_input1, curr_distance_input1
    global prev_distance_input2, curr_distance_input2
    global prev_distance_output, curr_distance_output
    global prev_distance_work, curr_distance_work

    if click_counter == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'Input1' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            input1_position = x, y
            click_counter = 1

    elif click_counter == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'Input2' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 150, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 150, 255), 2)
            input2_position = x, y
            click_counter = 2

    elif click_counter == 2:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'Output' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 80, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 80, 255), 2)
            output_position = x, y
            click_counter = 3

    elif click_counter == 3:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'Working' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (150, 80, 255))
            cv2.circle(image_frame, (x, y), 2, (150, 80, 255), 2)
            work_position = x, y
            click_counter = 4

    elif click_counter == 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            prev_position = x, y
            curr_position = x, y
            prev_distance_input1 = curr_distance_input1 = calculate_distance(input1_position, (x, y))
            prev_distance_input2 = curr_distance_input2 = calculate_distance(input2_position, (x, y))
            prev_distance_output = curr_distance_output = calculate_distance(output_position, (x, y))
            prev_distance_work = curr_distance_work = calculate_distance(work_position, (x, y))
            boundary = [x - 10, y - 10, x + 10, y + 10]
            click_counter = 5

    elif click_counter == 5:
        if boundary[0] <= x <= boundary[2] and boundary[1] <= y <= boundary[3]:
            pass
        else:
            boundary = [x - 10, y - 10, x + 10, y + 10]
            tracking(x, y)


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


def __find_max_min(list):
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
    min_x, max_x, min_y, max_y = __find_max_min(list)
    min_x -= rectangle_extender
    min_y -= rectangle_extender
    max_x += rectangle_extender
    max_y += rectangle_extender
    return min_x, min_y, max_x, max_y


def tracking(x, y):
    global image_frame, minimum_distance, calibrate_area_status, rectangle_extender
    global input1_calibrate_time, input2_calibrate_time, output_calibrate_time, work_calibrate_time
    global input1_position, input2_position, output_position, work_position
    global prev_position, curr_position, prev_direction, curr_direction
    global prev_distance_input1, curr_distance_input1, prev_direction_input1, curr_direction_input1
    global prev_distance_input2, curr_distance_input2, prev_direction_input2, curr_direction_input2
    global prev_distance_output, curr_distance_output, prev_direction_output, curr_direction_output
    global prev_distance_work, curr_distance_work, prev_direction_work, curr_direction_work
    global count_approaching_input1, count_approaching_input2, count_approaching_output, count_approaching_work
    global input1_list, input2_list, output_list, work_list
    global input1_calibrate_status, input2_calibrate_status, output_calibrate_status, work_calibrate_status

    # set current point position and direction to previous
    prev_direction = curr_direction
    prev_position = curr_position
    curr_position = x, y

    # calculate difference between current point and previous point
    diff_x = curr_position[0] - prev_position[0]
    diff_y = curr_position[1] - prev_position[1]

    # set current distance to previous
    prev_distance_input1 = curr_distance_input1
    prev_distance_input2 = curr_distance_input2
    prev_distance_output = curr_distance_output
    prev_distance_work = curr_distance_work

    # set current direction to previous
    prev_direction_input1 = curr_direction_input1
    prev_direction_input2 = curr_direction_input2
    prev_direction_output = curr_direction_output
    prev_direction_work = curr_direction_work

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
    curr_distance_input1 = calculate_distance(input1_position, (x, y))
    curr_distance_input2 = calculate_distance(input2_position, (x, y))
    curr_distance_output = calculate_distance(output_position, (x, y))
    curr_distance_work = calculate_distance(work_position, (x, y))

    # find direction number
    curr_direction = find_direction_number(point_direction_degree)
    curr_direction_input1 = find_direction_number(direction_input1_degree)
    curr_direction_input2 = find_direction_number(direction_input2_degree)
    curr_direction_output = find_direction_number(direction_output_degree)
    curr_direction_work = find_direction_number(direction_work_degree)

    # increase counter when approaching area with lower distance and not change direction
    # except work area due to many direction to approaching. it's use only distance
    if prev_distance_input1 > curr_distance_input1 and curr_direction_input1 == curr_direction:
        count_approaching_input1 += 1

    if prev_distance_input2 > curr_distance_input2 and curr_direction_input2 == curr_direction:
        count_approaching_input2 += 1

    if prev_distance_output > curr_distance_output and curr_direction_output == curr_direction:
        count_approaching_output += 1

    if prev_distance_work > curr_distance_work:
        count_approaching_work += 1

    # do this when direction is changed
    if curr_direction != prev_direction:

        # temp variable
        # create temp list to keep counter and find index that has maximum counter that mean maximum approach
        max_approaching_list = [count_approaching_input1, count_approaching_input2, count_approaching_output,
                                count_approaching_work]
        max_approaching = max_approaching_list.index(max(max_approaching_list))

        # approached input1
        if max_approaching == 0:
            if curr_distance_input1 <= minimum_distance:
                cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
                cv2.putText(image_frame, str((x, y, 'Input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 0, 255))
                if calibrate_area_status:
                    if input1_calibrate_status == 0:
                        if len(input1_list) < input1_calibrate_time:
                            input1_list.append((x, y))
                        else:
                            input1_calibrate_status = 1

        # approached input2
        elif max_approaching == 1:
            if curr_distance_input2 <= minimum_distance:
                cv2.circle(image_frame, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(image_frame, str((x, y, 'Input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if calibrate_area_status:
                    if input2_calibrate_status == 0:
                        if len(input2_list) < input2_calibrate_time:
                            input2_list.append((x, y))
                        else:
                            input2_calibrate_status = 1

        # approached output
        elif max_approaching == 2:
            if curr_distance_output <= minimum_distance:
                cv2.circle(image_frame, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(image_frame, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 80, 255))
                if calibrate_area_status:
                    if output_calibrate_status == 0:
                        if len(output_list) < output_calibrate_time:
                            output_list.append((x, y))
                        else:
                            output_calibrate_status = 1

        # approached work
        elif max_approaching == 3:
            if curr_distance_work <= minimum_distance:
                cv2.circle(image_frame, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(image_frame, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if calibrate_area_status:
                    if work_calibrate_status == 0:
                        if len(work_list) < work_calibrate_time:
                            work_list.append((x, y))
                        else:
                            work_calibrate_status = 1

        # reset approach counter after change direction
        count_approaching_input1 = count_approaching_input2 = count_approaching_output = count_approaching_work = 0

    if input1_calibrate_status == 1:
        x1, y1, x2, y2 = process_rectangle(input1_list)
        cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # stop calibrate and clear list
        input1_calibrate_status = -1
        input1_list.clear()

    if input2_calibrate_status == 1:
        x1, y1, x2, y2 = process_rectangle(input2_list)
        cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)
        # stop calibrate and clear list
        input2_calibrate_status = -1
        input2_list.clear()

    if output_calibrate_status == 1:
        x1, y1, x2, y2 = process_rectangle(output_list)
        cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 80, 255), 2)
        # stop calibrate and clear list
        output_calibrate_status = -1
        output_list.clear()

    if work_calibrate_status == 1:
        x1, y1, x2, y2 = process_rectangle(work_list)
        cv2.rectangle(image_frame, (x1, y1), (x2, y2), (150, 80, 255), 2)
        # stop calibrate and clear list
        work_calibrate_status = -1
        work_list.clear()

    # check if all area is finished calibrate set calibrate status to False and reset each area to prepare new calibrate
    if input1_calibrate_status == input2_calibrate_status == output_calibrate_status == work_calibrate_status == -1:
        calibrate_area_status = False
        input1_calibrate_status = input2_calibrate_status = output_calibrate_status = work_calibrate_status = 0
        print('all area has been drawn')


if __name__ == "__main__":
    while True:
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
