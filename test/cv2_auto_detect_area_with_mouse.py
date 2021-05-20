# Test automatically create rectangle over work area
# distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
import cv2
import math

# file_name = '../resources/videos/Full_Working1.mp4'
image_frame = cv2.imread('../resources/images/black_background.png')
boundary = [-1, -1, -1, -1]
input_boundary = [-1, -1, -1, -1]
point_list = []
distance_input1 = []
distance_input2 = []
distance_output = []
distance_work = []
input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)
is_first_click = 0
prev = -1
curr = -1
prev_status = -1
curr_status = -1
is_learning = True
rectangle_extender = 1.0
reduce_average = 1.0


def get_distance(origin, points):
    return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def tracking(x, y):
    global prev, curr, image_frame, prev_status, curr_status, point_list, input_boundary, is_learning
    prev = curr
    curr = x, y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    result = degree(math.atan2(diff_y, diff_x))

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

    if result >= 250 and result < 290:
        # print('UP')
        curr_status = 1

    elif result >= 290 and result < 340:
        # print('Q1')
        curr_status = 2

    elif result >= 340 and result < 360:
        # print('RIGHT')
        curr_status = 3

    elif result >= 0 and result < 20:
        # print('RIGHT')
        curr_status = 3

    elif result >= 20 and result < 70:
        # print('Q4')
        curr_status = 5

    elif result >= 70 and result < 110:
        # print('DOWN')
        curr_status = 6

    elif result >= 110 and result < 160:
        # print('Q3')
        curr_status = 7

    elif result >= 160 and result < 200:
        # print('LEFT')
        curr_status = 8

    elif result >= 200 and result < 250:
        # print('Q2')
        curr_status = 9

    if curr_status != prev_status:
        cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)
        cv2.putText(image_frame, str((x, y)), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0))
        if not len(point_list) == 15:
            point_list.append((x, y))
        elif is_learning:
            calculate_area()
            print('finished calculate')
            is_learning = False


def calculate_area():
    global image_frame
    global point_list, distance_input1, distance_input2, distance_work, distance_output
    global input1_position, input2_position, output_position, work_position

    # calculate distance for all points with marked area
    for i in range(len(point_list)):
        distance_input1.append((get_distance(input1_position, point_list[i]), i))
        distance_input2.append((get_distance(input2_position, point_list[i]), i))
        distance_output.append((get_distance(output_position, point_list[i]), i))
        distance_work.append((get_distance(work_position, point_list[i]), i))

    # calculate average distance
    average_distance_input1 = 0
    average_distance_input2 = 0
    average_distance_output = 0
    average_distance_work = 0
    for i in range(len(point_list)):
        average_distance_input1 += distance_input1[i][0]
        average_distance_input2 += distance_input2[i][0]
        average_distance_output += distance_output[i][0]
        average_distance_work += distance_work[i][0]
    average_distance_input1 = int(average_distance_input1 / len(distance_input1))
    average_distance_input2 = int(average_distance_input2 / len(distance_input2))
    average_distance_output = int(average_distance_output / len(distance_output))
    average_distance_work = int(average_distance_work / len(distance_work))

    # find close range of marked area
    temp_input1 = []
    temp_input2 = []
    temp_output = []
    temp_work = []
    for i in range(len(point_list)):
        if distance_input1[i][0] < average_distance_input1*reduce_average:
            temp_input1.append(point_list[distance_input1[i][1]])
        if distance_input2[i][0] < average_distance_input2*reduce_average:
            temp_input2.append(point_list[distance_input2[i][1]])
        if distance_output[i][0] < average_distance_output*reduce_average:
            temp_output.append(point_list[distance_output[i][1]])
        if distance_work[i][0] < average_distance_work*reduce_average:
            temp_work.append(point_list[distance_work[i][1]])

    # find average point around area input1
    sum_x = 0
    sum_y = 0
    temp_min_x = temp_input1[0][0]
    temp_max_x = temp_input1[0][0]
    temp_min_y = temp_input1[0][1]
    temp_max_y = temp_input1[0][1]

    for i in range(len(temp_input1)):
        sum_x += temp_input1[i][0]
        sum_y += temp_input1[i][1]
        if temp_input1[i][0] >= temp_max_x:
            temp_max_x = temp_input1[i][0]
        if temp_input1[i][0] <= temp_min_x:
            temp_min_x = temp_input1[i][0]
        if temp_input1[i][1] >= temp_max_y:
            temp_max_y = temp_input1[i][1]
        if temp_input1[i][1] <= temp_min_y:
            temp_min_y = temp_input1[i][1]
    center_input1 = (int(sum_x / len(temp_input1)), int(sum_y / len(temp_input1)))
    x1 = int(center_input1[0] - (center_input1[0] - temp_min_x) * rectangle_extender)
    y1 = int(center_input1[1] - (center_input1[1] - temp_min_y) * rectangle_extender)
    x2 = int(center_input1[0] + (temp_max_x - center_input1[0]) * rectangle_extender)
    y2 = int(center_input1[1] + (temp_max_y - center_input1[1]) * rectangle_extender)
    cv2.circle(image_frame, center_input1, 2, (0, 0, 255), 5)
    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # find average point around area input2
    sum_x = 0
    sum_y = 0
    temp_min_x = temp_input2[0][0]
    temp_max_x = temp_input2[0][0]
    temp_min_y = temp_input2[0][1]
    temp_max_y = temp_input2[0][1]

    for i in range(len(temp_input2)):
        sum_x += temp_input2[i][0]
        sum_y += temp_input2[i][1]
        if temp_input2[i][0] >= temp_max_x:
            temp_max_x = temp_input2[i][0]
        if temp_input2[i][0] <= temp_min_x:
            temp_min_x = temp_input2[i][0]
        if temp_input2[i][1] >= temp_max_y:
            temp_max_y = temp_input2[i][1]
        if temp_input2[i][1] <= temp_min_y:
            temp_min_y = temp_input2[i][1]
    center_input2 = (int(sum_x / len(temp_input2)), int(sum_y / len(temp_input2)))
    x1 = int(center_input2[0] - (center_input2[0] - temp_min_x) * rectangle_extender)
    y1 = int(center_input2[1] - (center_input2[1] - temp_min_y) * rectangle_extender)
    x2 = int(center_input2[0] + (temp_max_x - center_input2[0]) * rectangle_extender)
    y2 = int(center_input2[1] + (temp_max_y - center_input2[1]) * rectangle_extender)
    cv2.circle(image_frame, center_input2, 2, (0, 150, 255), 5)
    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)

    # find average point around area output
    sum_x = 0
    sum_y = 0
    temp_min_x = temp_output[0][0]
    temp_max_x = temp_output[0][0]
    temp_min_y = temp_output[0][1]
    temp_max_y = temp_output[0][1]
    for i in range(len(temp_output)):
        sum_x += temp_output[i][0]
        sum_y += temp_output[i][1]
        if temp_output[i][0] >= temp_max_x:
            temp_max_x = temp_output[i][0]
        if temp_output[i][0] <= temp_min_x:
            temp_min_x = temp_output[i][0]
        if temp_output[i][1] >= temp_max_y:
            temp_max_y = temp_output[i][1]
        if temp_output[i][1] <= temp_min_y:
            temp_min_y = temp_output[i][1]
    center_output = (int(sum_x / len(temp_output)), int(sum_y / len(temp_output)))
    x1 = int(center_output[0] - (center_output[0] - temp_min_x) * rectangle_extender)
    y1 = int(center_output[1] - (center_output[1] - temp_min_y) * rectangle_extender)
    x2 = int(center_output[0] + (temp_max_x - center_output[0]) * rectangle_extender)
    y2 = int(center_output[1] + (temp_max_y - center_output[1]) * rectangle_extender)
    cv2.circle(image_frame, center_output, 2, (0, 80, 255), 5)
    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 80, 255), 2)

    # find average point around area work
    sum_x = 0
    sum_y = 0
    temp_min_x = temp_work[0][0]
    temp_max_x = temp_work[0][0]
    temp_min_y = temp_work[0][1]
    temp_max_y = temp_work[0][1]
    for i in range(len(temp_work)):
        sum_x += temp_work[i][0]
        sum_y += temp_work[i][1]
        if temp_work[i][0] >= temp_max_x:
            temp_max_x = temp_work[i][0]
        if temp_work[i][0] <= temp_min_x:
            temp_min_x = temp_work[i][0]
        if temp_work[i][1] >= temp_max_y:
            temp_max_y = temp_work[i][1]
        if temp_work[i][1] <= temp_min_y:
            temp_min_y = temp_work[i][1]
    center_work = (int(sum_x / len(temp_work)), int(sum_y / len(temp_work)))
    x1 = int(center_work[0] - (center_work[0] - temp_min_x) * rectangle_extender)
    y1 = int(center_work[1] - (center_work[1] - temp_min_y) * rectangle_extender)
    x2 = int(center_work[0] + (temp_max_x - center_work[0]) * rectangle_extender)
    y2 = int(center_work[1] + (temp_max_y - center_work[1]) * rectangle_extender)
    cv2.circle(image_frame, center_work, 2, (150, 80, 255), 5)
    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (150, 80, 255), 2)

    print('End of calculate')

def mouse_click(event, x, y, flags, param):
    global image_frame, is_first_click, prev, curr, boundary, input_boundary
    global input1_position, input2_position, output_position, work_position

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
            boundary = [x - 15, y - 15, x + 15, y + 15]
            is_first_click = False
            is_first_click = 5

    elif is_first_click == 5:
        if x >= boundary[0] and x <= boundary[2] and y >= boundary[1] and y <= boundary[3]:
            pass
        else:
            boundary = [x - 15, y - 15, x + 15, y + 15]
            tracking(x, y)

    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        is_first_click = 0


if __name__ == "__main__":

    while True:
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
