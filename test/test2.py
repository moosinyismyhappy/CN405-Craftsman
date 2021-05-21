# new method for auto detect area (Mouse)

import cv2
import math

# file_name = '../resources/videos/Full_Working1.mp4'
image_frame = cv2.imread('../resources/images/black_background.png')
boundary = [-1, -1, -1, -1]
is_first_click = 0
prev = -1
curr = -1
prev_status = -1
curr_status = -1
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
input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)
count_approach_input1 = 0
count_approach_input2 = 0
count_approach_output = 0
count_approach_work = 0
input1_list = []
input2_list = []
output_list = []
work_list = []
is_input1_ready = 0
is_input2_ready = 0
is_output_ready = 0
is_work_ready = 0


def mouse_click(event, x, y, flags, param):
    global image_frame, is_first_click, prev, curr, boundary
    global input1_position, input2_position, output_position, work_position
    global prev_distance_input1, curr_distance_input1
    global prev_distance_input2, curr_distance_input2
    global prev_distance_output, curr_distance_output
    global prev_distance_work, curr_distance_work

    if is_first_click == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'input1' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            input1_position = x, y
            print('input1 position ', x, y)
            is_first_click = 1

    elif is_first_click == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'input2' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 150, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 150, 255), 2)
            input2_position = x, y
            print('input2 position ', x, y)
            is_first_click = 2

    elif is_first_click == 2:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'output' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 80, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 80, 255), 2)
            output_position = x, y
            print('output position ', x, y)
            is_first_click = 3

    elif is_first_click == 3:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'working' + str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (150, 80, 255))
            cv2.circle(image_frame, (x, y), 2, (150, 80, 255), 2)
            work_position = x, y
            print('work position ', x, y)
            is_first_click = 4

    elif is_first_click == 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            prev = x, y
            curr = x, y
            prev_distance_input1 = curr_distance_input1 = get_distance(input1_position, (x, y))
            prev_distance_input2 = curr_distance_input2 = get_distance(input2_position, (x, y))
            prev_distance_output = curr_distance_output = get_distance(output_position, (x, y))
            prev_distance_work = curr_distance_work = get_distance(work_position, (x, y))
            boundary = [x - 10, y - 10, x + 10, y + 10]
            is_first_click = False
            is_first_click = 5

    elif is_first_click == 5:
        if x >= boundary[0] and x <= boundary[2] and y >= boundary[1] and y <= boundary[3]:
            pass
        else:
            boundary = [x - 10, y - 10, x + 10, y + 10]
            tracking(x, y)
    # cv2.rectangle(image_frame,(boundary[0],boundary[1]),(boundary[2],boundary[3]),(255,255,255),2)

    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        is_first_click = 0


def get_distance(origin, points):
    return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def find_direction_degree(degree):
    ########################################
    #          240    UP    300            #
    #                                      #
    #                                      #
    #     Q2                        Q1     #
    #                                      #
    #                                      #
    # 180           ORIGIN            000  #
    #                                      #
    #                                      #
    #     Q3                        Q4     #
    #                                      #
    #                                      #
    #          120   DOWN    60            #
    ########################################
    if 240 <= degree < 300:
        return 1
    elif 300 <= degree < 360:
        return 2
    elif 0 <= degree < 60:
        return 3
    elif 60 <= degree < 120:
        return 4
    elif 120 <= degree < 180:
        return 5
    elif 180 <= degree < 240:
        return 6


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


def tracking(x, y):
    global image_frame, prev_status, curr_status, curr, prev,boundary_extender
    global input1_position, input2_position, output_position, work_position
    global prev_distance_input1, curr_distance_input1
    global prev_distance_input2, curr_distance_input2
    global prev_distance_output, curr_distance_output
    global prev_distance_work, curr_distance_work
    global prev_direction_input1, curr_direction_input1
    global prev_direction_input2, curr_direction_input2
    global prev_direction_output, curr_direction_output
    global prev_direction_work, curr_direction_work
    global count_approach_input1, count_approach_input2, count_approach_output, count_approach_work
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

    prev = curr
    curr = x, y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    point_direction_degree = degree(math.atan2(diff_y, diff_x))

    curr_status = find_direction_degree(point_direction_degree)
    curr_direction_input1 = find_direction_degree(direction_input1_degree)
    curr_direction_input2 = find_direction_degree(direction_input2_degree)
    curr_direction_output = find_direction_degree(direction_output_degree)
    curr_direction_work = find_direction_degree(direction_work_degree)

    print(direction_input1_degree, direction_input2_degree, direction_output_degree, direction_work_degree)

    # increase counter when approach and same direction that area
    if prev_distance_input1 > curr_distance_input1 and curr_direction_input1 == curr_status:
        # print('approach input1', prev_direction_input1, curr_direction_input1)
        count_approach_input1 += 1

    if prev_distance_input2 > curr_distance_input2 and curr_direction_input2 == curr_status:
        # print('approach input2', prev_direction_input2, curr_direction_input2)
        count_approach_input2 += 1

    if prev_distance_output > curr_distance_output and curr_direction_output == curr_status:
        # print('approach output', prev_direction_output, curr_direction_output)
        count_approach_output += 1

    if prev_distance_work > curr_distance_work and curr_direction_work == curr_status:
        # print('approach work', prev_direction_work, curr_direction_work)
        count_approach_work += 1

    if curr_status != prev_status:
        temp = [count_approach_input1, count_approach_input2, count_approach_output, count_approach_work]
        max_temp = temp.index(max(temp))

        if max_temp == 0:
            if curr_distance_input1 <= 80:
                cv2.circle(image_frame, (x, y), 2, (255, 255, 255), 2)
                cv2.putText(image_frame, str((x, y, 'input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (255, 255, 255))
                if is_input1_ready == 0:
                    if len(input1_list) < 10:
                        input1_list.append((x, y))
                    else:
                        is_input1_ready = 1
                elif is_input1_ready == 1:
                    print('draw input1 area')
                    average_x, average_y = find_average_point(input1_list)
                    min_x, max_x, min_y, max_y = find_max_min(input1_list)
                    x1 = average_x - (average_x - min_x)
                    y1 = average_y - (average_y - min_y)
                    x2 = average_x + (max_x - average_x)
                    y2 = average_y + (max_y - average_y)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (0, 0, 255), 2)
                    is_input1_ready = -1

        elif max_temp == 1:
            if curr_distance_input2 <= 80:
                cv2.circle(image_frame, (x, y), 2, (0, 150, 255), 2)
                cv2.putText(image_frame, str((x, y, 'input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (0, 150, 255))
                if is_input2_ready == 0:
                    if len(input2_list) < 10:
                        input2_list.append((x, y))
                    else:
                        is_input2_ready = 1
                elif is_input2_ready == 1:
                    average_x, average_y = find_average_point(input2_list)
                    min_x, max_x, min_y, max_y = find_max_min(input2_list)
                    x1 = average_x - (average_x - min_x)
                    y1 = average_y - (average_y - min_y)
                    x2 = average_x + (max_x - average_x)
                    y2 = average_y + (max_y - average_y)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (0, 150, 255), 2)
                    is_input2_ready = -1

        elif max_temp == 2:
            if curr_distance_output <= 80:
                cv2.circle(image_frame, (x, y), 2, (0, 80, 255), 2)
                cv2.putText(image_frame, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
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
                    x1 = average_x - (average_x - min_x)
                    y1 = average_y - (average_y - min_y)
                    x2 = average_x + (max_x - average_x)
                    y2 = average_y + (max_y - average_y)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (0, 80, 255), 2)
                    is_output_ready = -1

        elif max_temp == 3:
            if curr_distance_work <= 80:
                cv2.circle(image_frame, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(image_frame, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if is_work_ready == 0:
                    if len(work_list) < 10:
                        work_list.append((x, y))
                    else:
                        is_work_ready = 1
                elif is_work_ready == 1:
                    print('draw work area')
                    average_x, average_y = find_average_point(work_list)
                    min_x, max_x, min_y, max_y = find_max_min(work_list)
                    x1 = average_x - (average_x - min_x)
                    y1 = average_y - (average_y - min_y)
                    x2 = average_x + (max_x - average_x)
                    y2 = average_y + (max_y - average_y)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2),
                                  (150, 80, 255), 2)
                    is_work_ready = -1

        count_approach_input1 = 0
        count_approach_input2 = 0
        count_approach_output = 0
        count_approach_work = 0


if __name__ == "__main__":
    while True:
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
