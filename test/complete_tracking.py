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
    curr = x, y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    result = degree(math.atan2(diff_y, diff_x))

    ##################
    #  Q2   270   Q1 #
    # 180        000 #
    #  Q3   090   Q4 #
    ##################

    if result >= 260 and result < 280:
        print('UP')
        curr_status = 0.5

    elif result >= 280 and result < 350:
        print('Q1')
        curr_status = 1

    elif result >= 350 and result < 360:
        print('RIGHT')
        curr_status = 1.5

    elif result >= 0 and result < 10:
        print('RIGHT')
        curr_status = 1.5

    elif result >= 10 and result < 80:
        print('Q4')
        curr_status = 4

    elif result >= 80 and result < 100:
        print('DOWN')
        curr_status = 4.5

    elif result >= 100 and result < 170:
        print('Q3')
        curr_status = 3

    elif result >= 170 and result < 190:
        print('LEFT')
        curr_status = 3.5

    elif result >= 190 and result < 260:
        print('Q2')
        curr_status = 2

    if curr_status != prev_status:
        image_frame = cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)


def mouse_click(event, x, y, flags, param):
    global image_frame, is_first_click, count, prev, curr

    if is_first_click:
        if event == cv2.EVENT_LBUTTONDOWN:
            prev = x, y
            curr = x, y
            is_first_click = False

    else:
        if count == 5:
            tracking(x, y)
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
