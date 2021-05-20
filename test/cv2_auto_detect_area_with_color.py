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
imageFrame = None
hsvFrame = None
click_state = 0
point_list = []
distance_input1 = []
distance_input2 = []
distance_output = []
distance_work = []
input1_position = (-1, -1)
input2_position = (-1, -1)
output_position = (-1, -1)
work_position = (-1, -1)
is_learning = True
number_of_learning = 100
average_reducer = 0.6
rectangle_extender = 1.15
boundary_detect_reducer = 15

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


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def tracking_left(new_center):
    global imageFrame, center_bound_left, is_first_detect_left, prev_left, curr_left, is_out_left
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
    global prev_left, curr_left, image_frame, prev_status_left, curr_status_left, black_img, is_learning, number_of_learning
    curr_left = x, y
    prev_status_left = curr_status_left

    diff_x = curr_left[0] - prev_left[0]
    diff_y = curr_left[1] - prev_left[1]

    result = degree(math.atan2(diff_y, diff_x))

    prev_left = curr_left

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
        curr_status_left = 1

    elif result >= 290 and result < 340:
        # print('Q1')
        curr_status_left = 2

    elif result >= 340 and result < 360:
        # print('RIGHT')
        curr_status_left = 3

    elif result >= 0 and result < 20:
        # print('RIGHT')
        curr_status_left = 3

    elif result >= 20 and result < 70:
        # print('Q4')
        curr_status_left = 5

    elif result >= 70 and result < 110:
        # print('DOWN')
        curr_status_left = 6

    elif result >= 110 and result < 160:
        # print('Q3')
        curr_status_left = 7

    elif result >= 160 and result < 200:
        # print('LEFT')
        curr_status_left = 8

    elif result >= 200 and result < 250:
        # print('Q2')
        curr_status_left = 9

    if curr_status_left != prev_status_left:
        cv2.circle(black_img, (x, y), 2, (0, 0, 255), 2)
        if not len(point_list) == number_of_learning:
            point_list.append((x, y))
        elif is_learning:
            calculate_area()
            print('finished calculate')
            is_learning = False


def tracking_right(new_center):
    global imageFrame, center_bound_right, is_first_detect_right, prev_right, curr_right, is_out_right
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
    global prev_right, curr_right, image_frame, prev_status_right, curr_status_right, black_img, is_learning, number_of_learning
    curr_right = x, y
    prev_status_right = curr_status_right

    diff_x = curr_right[0] - prev_right[0]
    diff_y = curr_right[1] - prev_right[1]

    result = degree(math.atan2(diff_y, diff_x))

    prev_right = curr_right

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
        curr_status_right = 1

    elif result >= 290 and result < 340:
        # print('Q1')
        curr_status_right = 2

    elif result >= 340 and result < 360:
        # print('RIGHT')
        curr_status_right = 3

    elif result >= 0 and result < 20:
        # print('RIGHT')
        curr_status_right = 3

    elif result >= 20 and result < 70:
        # print('Q4')
        curr_status_right = 5

    elif result >= 70 and result < 110:
        # print('DOWN')
        curr_status_right = 6

    elif result >= 110 and result < 160:
        # print('Q3')
        curr_status_right = 7

    elif result >= 160 and result < 200:
        # print('LEFT')
        curr_status_right = 8

    elif result >= 200 and result < 250:
        # print('Q2')
        curr_status_right = 9

    if curr_status_right != prev_status_right:
        cv2.circle(black_img, (x, y), 2, (0, 255, 255), 2)
        if not len(point_list) == number_of_learning:
            point_list.append((x, y))
        elif is_learning:
            calculate_area()
            print('finished calculate')
            is_learning = False


def get_distance(origin, points):
    return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))


def calculate_area():
    global image_frame, average_reducer
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
        if distance_input1[i][0] < average_distance_input1 * average_reducer:
            temp_input1.append(point_list[distance_input1[i][1]])
        if distance_input2[i][0] < average_distance_input2 * average_reducer:
            temp_input2.append(point_list[distance_input2[i][1]])
        if distance_output[i][0] < average_distance_output * average_reducer:
            temp_output.append(point_list[distance_output[i][1]])
        if distance_work[i][0] < average_distance_work * average_reducer:
            temp_work.append(point_list[distance_work[i][1]])

    print(temp_input1, temp_input2, temp_output, temp_work)

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
    cv2.circle(black_img, center_input1, 2, (0, 0, 255), 5)
    cv2.rectangle(black_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

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
    cv2.circle(black_img, center_input2, 2, (0, 150, 255), 5)
    cv2.rectangle(black_img, (x1, y1), (x2, y2), (0, 150, 255), 2)

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
    cv2.circle(black_img, center_output, 2, (0, 80, 255), 5)
    cv2.rectangle(black_img, (x1, y1), (x2, y2), (0, 80, 255), 2)

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
    cv2.circle(black_img, center_work, 2, (150, 80, 255), 8)
    cv2.rectangle(black_img, (x1, y1), (x2, y2), (150, 80, 255), 2)

    print('End of calculate')


if __name__ == "__main__":

    # Capturing video through webcam
    #webcam = cv2.VideoCapture(file_name)
    webcam = cv2.VideoCapture(1)
    while True:
        # Receive stream image from camera
        _, imageFrame = webcam.read()
        imageFrame = cv2.resize(imageFrame, (640, 480))
        # imageFrame = cv2.flip(imageFrame, 1)

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
                center = int((2 * x + w) / 2), int((2 * y + h) / 2)

                # step one : draw static rectangle over first detect area
                if is_first_detect_left == 0:
                    center_bound_left[0] = x+boundary_detect_reducer
                    center_bound_left[1] = y+boundary_detect_reducer
                    center_bound_left[2] = x+w-boundary_detect_reducer
                    center_bound_left[3] = y+h-boundary_detect_reducer
                    curr_left = center
                    prev_left = center
                    prev_status_left = -1
                    curr_status_left = -1
                    is_first_detect_left = 1
                elif is_first_detect_left == 1:
                    tracking_left(center)
                    if is_out_left:
                        center_bound_left[0] = x+boundary_detect_reducer
                        center_bound_left[1] = y+boundary_detect_reducer
                        center_bound_left[2] = x+w-boundary_detect_reducer
                        center_bound_left[3] = y+h-boundary_detect_reducer

                imageFrame = cv2.rectangle(imageFrame, (center_bound_left[0], center_bound_left[1]),
                                           (center_bound_left[2], center_bound_left[3]),
                                           (0, 255, 0), 2)
                imageFrame = cv2.circle(imageFrame, center, 2, (0, 0, 255), 2)
                cv2.putText(imageFrame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))
                imageFrame = cv2.rectangle(imageFrame, (x, y),
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
                    center_bound_right[0] = x+boundary_detect_reducer
                    center_bound_right[1] = y+boundary_detect_reducer
                    center_bound_right[2] = x+w-boundary_detect_reducer
                    center_bound_right[3] = y+h-boundary_detect_reducer
                    curr_right = center
                    prev_right = center
                    prev_status_right = -1
                    curr_status_right = -1
                    is_first_detect_right = 1
                elif is_first_detect_right == 1:
                    tracking_right(center)
                    if is_out_right:
                        center_bound_right[0] = x+boundary_detect_reducer
                        center_bound_right[1] = y+boundary_detect_reducer
                        center_bound_right[2] = x+w-boundary_detect_reducer
                        center_bound_right[3] = y+h-boundary_detect_reducer

                imageFrame = cv2.rectangle(imageFrame, (center_bound_right[0], center_bound_right[1]),
                                           (center_bound_right[2], center_bound_right[3]),
                                           (0, 255, 0), 2)
                imageFrame = cv2.circle(imageFrame, center, 2, (0, 0, 255), 2)
                cv2.putText(imageFrame, str(center), center,
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (255, 255, 255))
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                           (x + w, y + h),
                                           (0, 255, 255), 2)

        final_image = cv2.addWeighted(imageFrame, 1.0, black_img, 1.0, 0)
        cv2.imshow("Multiple color Detection", final_image)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(15) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()
