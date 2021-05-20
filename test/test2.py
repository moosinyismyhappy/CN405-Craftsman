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


def tracking(x, y):
    global prev, curr, image_frame, prev_status, curr_status
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
    global is_input1_ready,is_input2_ready,is_output_ready,is_work_ready

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
    direction_input1 = degree(math.atan2(input1_position[1] - y, input1_position[0] - x))
    direction_input2 = degree(math.atan2(input2_position[1] - y, input2_position[0] - x))
    direction_output = degree(math.atan2(output_position[1] - y, output_position[0] - x))
    direction_work = degree(math.atan2(work_position[1] - y, work_position[0] - x))

    prev_direction_input1 = curr_direction_input1
    prev_direction_input2 = curr_direction_input2
    prev_direction_output = curr_direction_output
    prev_direction_work = curr_direction_work

    prev = curr
    curr = x, y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    result = degree(math.atan2(diff_y, diff_x))

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

    # direction of point
    if 240 <= result < 300:
        curr_status = 1

    elif 300 <= result < 360:
        curr_status = 2

    elif 0 <= result < 60:
        curr_status = 3

    elif 60 <= result < 120:
        curr_status = 4

    elif 120 <= result < 180:
        curr_status = 5

    elif 180 <= result < 240:
        curr_status = 6

    # direction of input1
    if 240 <= direction_input1 < 300:
        curr_direction_input1 = 1

    elif 300 <= direction_input1 < 360:
        curr_direction_input1 = 2

    elif 0 <= direction_input1 < 60:
        curr_direction_input1 = 3

    elif 60 <= direction_input1 < 120:
        curr_direction_input1 = 4

    elif 120 <= direction_input1 < 180:
        curr_direction_input1 = 5

    elif 180 <= direction_input1 < 240:
        curr_direction_input1 = 6

    # direction of input2
    if 240 <= direction_input2 < 300:
        curr_direction_input2 = 1

    elif 300 <= direction_input2 < 360:
        curr_direction_input2 = 2

    elif 0 <= direction_input2 < 60:
        curr_direction_input2 = 3

    elif 60 <= direction_input2 < 120:
        curr_direction_input2 = 4

    elif 120 <= direction_input1 < 180:
        curr_direction_input2 = 5

    elif 180 <= direction_input1 < 240:
        curr_direction_input2 = 6

    # direction of output
    if 240 <= direction_output < 300:
        curr_direction_output = 1

    elif 300 <= direction_output < 360:
        curr_direction_output = 2

    elif 0 <= direction_output < 60:
        curr_direction_output = 3

    elif 60 <= direction_output < 120:
        curr_direction_output = 4

    elif 120 <= direction_output < 180:
        curr_direction_output = 5

    elif 180 <= direction_output < 240:
        curr_direction_output = 6

    # direction of work
    if 240 <= direction_work < 300:
        curr_direction_work = 1

    elif 300 <= direction_work < 360:
        curr_direction_work = 2

    elif 0 <= direction_work < 60:
        curr_direction_work = 3

    elif 60 <= direction_work < 120:
        curr_direction_work = 4

    elif 120 <= direction_work < 180:
        curr_direction_work = 5

    elif 180 <= direction_work < 240:
        curr_direction_work = 6

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
            cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)
            cv2.putText(image_frame, str((x, y, 'input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        (255, 255, 0))
            if is_input1_ready == 0:
                if len(input1_list) < 10:
                    input1_list.append((x, y))
                else:
                    is_input1_ready = 1
            elif is_input1_ready == 1:
                print('draw rectangle input1')
                temp_sum_x = 0
                temp_sum_y = 0
                for i in input1_list:
                    temp_sum_x += i[0]
                    temp_sum_y += i[1]
                temp_sum_x = int(temp_sum_x/len(input1_list))
                temp_sum_y = int(temp_sum_y / len(input1_list))
                cv2.rectangle(image_frame, (temp_sum_x-50, temp_sum_y-50), (temp_sum_x+50, temp_sum_y+50), (0, 0, 255), 2)
                is_input1_ready = -1


        elif max_temp == 1:
            cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)
            cv2.putText(image_frame, str((x, y, 'input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        (255, 255, 0))
            if is_input2_ready == 0:
                if len(input2_list) < 10:
                    input2_list.append((x, y))
                else:
                    is_input2_ready = 1
            elif is_input2_ready == 1:
                temp_sum_x = 0
                temp_sum_y = 0
                for i in input2_list:
                    temp_sum_x += i[0]
                    temp_sum_y += i[1]
                temp_sum_x = int(temp_sum_x / len(input2_list))
                temp_sum_y = int(temp_sum_y / len(input2_list))
                cv2.rectangle(image_frame, (temp_sum_x - 50, temp_sum_y - 50), (temp_sum_x + 50, temp_sum_y + 50),
                              (0, 150, 255), 2)
                is_input2_ready = -1

        elif max_temp == 2:
            cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)
            cv2.putText(image_frame, str((x, y, 'output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        (255, 255, 0))
            if is_output_ready == 0:
                if len(output_list) < 10:
                    output_list.append((x, y))
                else:
                    is_output_ready = 1
            elif is_output_ready == 1:
                print('draw rectangle output')
                temp_sum_x = 0
                temp_sum_y = 0
                for i in output_list:
                    temp_sum_x += i[0]
                    temp_sum_y += i[1]
                temp_sum_x = int(temp_sum_x / len(output_list))
                temp_sum_y = int(temp_sum_y / len(output_list))
                cv2.rectangle(image_frame, (temp_sum_x - 50, temp_sum_y - 50), (temp_sum_x + 50, temp_sum_y + 50),
                              (0, 80, 255), 2)
                is_output_ready = -1

        elif max_temp == 3:
            cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)
            cv2.putText(image_frame, str((x, y, 'work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        (255, 255, 0))
            if is_work_ready == 0:
                if len(work_list) < 10:
                    work_list.append((x, y))
                else:
                    is_work_ready = 1
            elif is_work_ready == 1:
                print('draw rectangle work')
                temp_sum_x = 0
                temp_sum_y = 0
                for i in work_list:
                    temp_sum_x += i[0]
                    temp_sum_y += i[1]
                temp_sum_x = int(temp_sum_x / len(work_list))
                temp_sum_y = int(temp_sum_y / len(work_list))
                cv2.rectangle(image_frame, (temp_sum_x - 50, temp_sum_y - 50), (temp_sum_x + 50, temp_sum_y + 50),
                              (80, 150, 255), 2)
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
