# new method for auto detect area (Mouse)

import cv2

# load image file
image_frame = cv2.imread('../resources/images/black_background.png')
click_counter = 0
x1 = -1
y1 = -1
x2 = -1
y2 = -1
rectangle_list = []
is_first_rectangle = True


def mouse_click(event, x, y, flags, param):
    global image_frame, click_counter, x1, y1, x2, y2, rectangle_list, is_first_rectangle

    if click_counter == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            if is_first_rectangle:
                cv2.putText(image_frame, str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255))
                cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
                x1, y1 = x, y
            else:
                x1, y1 = x, y
            # set new counter to get x2,y2
            click_counter = 1

    elif click_counter == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            if is_first_rectangle:
                cv2.putText(image_frame, str((x, y)), (x - 15, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255))
                cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
                x2, y2 = x, y
                cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)
                rectangle_list.append((x1, y1, x2, y2))
                is_first_rectangle = False
            else:
                rectangle1 = rectangle_list[0]
                x2, y2 = x, y
                rectangle2 = [x1, y1, x2, y2]
                result = is_rectangle_overlap(rectangle1, rectangle2)
                if not result:
                    print('No overlap , Rectangle created ...')
                    cv2.putText(image_frame, str((x1, y1)), (x1 - 15, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))
                    cv2.circle(image_frame, (x1, y1), 2, (0, 0, 255), 2)
                    cv2.putText(image_frame, str((x2, y2)), (x2 - 15, y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))
                    cv2.circle(image_frame, (x2, y2), 2, (0, 0, 255), 2)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)
                    # add no overlap rectangle to list
                    rectangle_list.append((x1, y1, x2, y2))
                else:
                    print('overlap , Calculating solution ')
                    result = where_rectangle_overlap(rectangle1, rectangle2)
                    overlap_resolution(result, rectangle1)

                    cv2.putText(image_frame, str((x1, y1)), (x1 - 15, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))
                    cv2.circle(image_frame, (x1, y1), 2, (0, 0, 255), 2)
                    cv2.putText(image_frame, str((x2, y2)), (x2 - 15, y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0, 0, 255))
                    cv2.circle(image_frame, (x2, y2), 2, (0, 0, 255), 2)
                    cv2.rectangle(image_frame, (x1, y1), (x2, y2), (0, 150, 255), 2)

                    # add no overlap rectangle to list
                    rectangle_list.append((x1, y1, x2, y2))

            # reset counter to get x1,y1
            click_counter = 0

    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        rectangle_list.clear()


def overlap_resolution(overlap_status, reference_rect):
    global x1, y1, x2, y2

    if overlap_status == 0:
        x2 = reference_rect[0] - 1
    elif overlap_status == 1:
        x1 = reference_rect[2] + 1
    elif overlap_status == 2:
        y2 = reference_rect[1] - 1
    elif overlap_status == 3:
        y1 = reference_rect[3] + 1
    elif overlap_status == 4:
        if x2 - x1 > y2 - y1:
            x2 = reference_rect[0] - 1
        else:
            y2 = reference_rect[1] - 1
    elif overlap_status == 5:
        if x1 - x2 > y1 - y2:
            x1 = reference_rect[2] + 1
        else:
            y2 = reference_rect[1] - 1

def is_rectangle_overlap(rect1, rect2):
    if (rect1[0] >= rect2[2]) or (rect1[2] <= rect2[0]) or (rect1[3] <= rect2[1]) or (rect1[1] >= rect2[3]):
        # no overlap occur
        return False
    else:
        # overlap occur
        return True


def where_rectangle_overlap(rect1, rect2):
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

    # overlap on only each side
    # overlap left
    if u1 < x1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        return 0
    # overlap right
    elif x1 < u1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        return 1
    # overlap top
    elif x1 < u1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        return 2
    # overlap bottom
    elif x1 < u1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        return 3

    # overlap on corner
    # overlap top-left
    elif u1 < x1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        return 4
    # overlap top-right
    elif x1 < u1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        return 5
    # overlap bottom-left
    elif u1 < x1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        return 6
    # overlap bottom-right
    elif x1 < u1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        return 7

    # overlap on vertical
    # overlap vertical-left
    elif u1 < x1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        return 8
    # overlap vertical-center
    elif x1 < u1 < u2 and v1 < y1 < v2 and u1 < u2 < x2 and v1 < y2 < v2:
        return 9
    # overlap vertical-right
    elif x1 < u1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        return 10

    # overlap on horizontal
    # overlap horizontal-top
    elif u1 < x1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        return 11
    # overlap horizontal-center
    elif u1 < x1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < v2 < y2:
        return 12
    # overlap horizontal-bottom
    elif u1 < x1 < u2 and y1 < v1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        return 13

    # overlap inside and outside
    # overlap inside other rectangle
    elif u1 < x1 < u2 and v1 < y1 < v2 and u1 < x2 < u2 and v1 < y2 < v2:
        return 14
    # overlap outside other rectangle
    elif x1 < u1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
        return 15


if __name__ == "__main__":
    while True:
        print(len(rectangle_list))
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
