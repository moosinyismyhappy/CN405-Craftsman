# test tracking (temp)

import cv2
import math

file_name = '../resources/videos/Full_Working1.mp4'
image_frame = cv2.imread('../resources/images/black_background.png')
is_first_click = True
count = 0
prev = -1
curr = -1
prev_status = -1
curr_status = -1


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def tracking(x, y):
    global prev, curr, image_frame, prev_status, curr_status

    prev = curr
    curr = x,y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    result = degree(math.atan2(diff_y, diff_x))

    ########################################
    #          240    UP    300            #
    #                                      #
    #      Q2                   Q1         #
    #                                      #
    #   210                        330     #
    #                                      #
    # LEFT          ORIGIN           RIGHT #
    #                                      #
    #   150                        030     #
    #                                      #
    #      Q3                   Q4         #
    #                                      #
    #          120   DOWN   060            #
    ########################################

    if result >= 240 and result < 300:
        print('UP')
        curr_status = 0.5

    elif result >= 300 and result < 330:
        print('Q1')
        curr_status = 1

    elif result >= 330 and result < 360:
        print('RIGHT')
        curr_status = 1.5

    elif result >= 0 and result < 30:
        print('RIGHT')
        curr_status = 1.5

    elif result >= 30 and result < 60:
        print('Q4')
        curr_status = 2

    elif result >= 60 and result < 120:
        print('DOWN')
        curr_status = 2.5

    elif result >= 120 and result < 150:
        print('Q3')
        curr_status = 3

    elif result >= 150 and result < 210:
        print('LEFT')
        curr_status = 3.5

    elif result >= 210 and result < 240:
        print('Q2')
        curr_status = 4

    if curr_status != prev_status:
        image_frame = cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)


def mouse_click(event, x, y, flags, param):
    global image_frame, is_first_click, prev, curr, prev_status,count

    if is_first_click:
        if event == cv2.EVENT_LBUTTONDOWN:
            prev = x, y
            curr = x, y
            is_first_click = False

    else:
        if count == 5:
            tracking(x,y)
            count = 0
        else:
            count = count + 1


    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        is_first_click = True


if __name__ == "__main__":

    while True:

        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
