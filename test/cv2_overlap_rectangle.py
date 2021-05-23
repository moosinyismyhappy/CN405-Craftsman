# new method for auto detect area (Mouse)

import cv2
import math

# load image file
image_frame = cv2.imread('../resources/images/black_background.png')
click_counter = 0
x1 = -1
y1 = -1
x2 = -1
y2 = -1
rectangle_list = []


def mouse_click(event, x, y, flags, param):
    global image_frame, click_counter, x1, y1, x2, y2, rectangle_list

    if click_counter == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            x1, y1 = x, y
            click_counter = 1

    elif click_counter == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            x2, y2 = x, y
            cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)
            click_counter = 0
            rectangle_list.append((x1, y1, x2, y2))

    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        rectangle_list.clear()


def is_rectangle_overlap(rect1, rect2):
    # rectangle1
    x1 = rect1[0]
    y1 = rect1[1]
    x2 = rect1[2]
    y2 = rect1[3]

    # rectangle2
    u1 = rect2[0]
    v1 = rect2[1]
    u2 = rect2[2]
    v2 = rect2[3]

    count_overlap = 0

    # overlap on only each side
    if u1 < x1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        print('overlap left')
        count_overlap += 1
    if x1 < u1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        print('overlap right')
        count_overlap += 1
    if x1 < u1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        print('overlap top')
        count_overlap += 1
    if x1 < u1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        print('overlap bottom')
        count_overlap += 1

    # overlap on corner
    if u1 < x1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        print('overlap top-left')
        count_overlap += 1
    if x1 < u1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        print('overlap top-right')
        count_overlap += 1
    if u1 < x1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        print('overlap bottom-left')
        count_overlap += 1
    if x1 < u1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        print('overlap bottom-right')
        count_overlap += 1

    # overlap on vertical
    if u1 < x1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        print('overlap vertical-left')
        count_overlap += 1
    if x1 < u1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        print('overlap vertical-center')
        count_overlap += 1
    if x1 < u1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        print('overlap vertical-right')
        count_overlap += 1

    # overlap on horizontal
    if u1 < x1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        print('overlap horizontal-top')
        count_overlap += 1
    if u1 < x1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        print('overlap horizontal-center')
        count_overlap += 1
    if u1 < x1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        print('overlap horizontal-bottom')
        count_overlap += 1

    # overlap inside and outside
    if u1 < x1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        print('overlap inside other rectangle')
        count_overlap += 1
    if x1 < u1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        print('overlap outside other rectangle')
        count_overlap += 1

    # count_overlap not equal zero mean overlap occur
    if count_overlap == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    while True:
        if len(rectangle_list) == 2:
            print(is_rectangle_overlap(rectangle_list[0], rectangle_list[1]))
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
