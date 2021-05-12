# Test automatically create rectangle over work area
# distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
import cv2
import math

file_name = '../resources/videos/Full_Working1.mp4'
image_frame = cv2.imread('../resources/images/black_background.png')
boundary = [-1, -1, -1, -1]
input_boundary = [-1,-1,-1,-1]
point_queue = []
center_input = (-1,-1)
is_first_click = 0
count = 0
prev = -1
curr = -1
prev_status = -1
curr_status = -1

def get_distance(points):
    global center_input
    return int(math.sqrt( ((points[0]-center_input[0])**2)+((points[1]-center_input[1])**2)))


def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)


def tracking(x, y):
    global prev, curr, image_frame, prev_status, curr_status,point_queue ,input_boundary
    prev = curr
    curr = x, y
    prev_status = curr_status

    diff_x = curr[0] - prev[0]
    diff_y = curr[1] - prev[1]

    result = degree(math.atan2(diff_y, diff_x))

    ########################################
    #          255    UP    285            #
    #                                      #
    #      Q2                   Q1         #
    #                                      #
    #   195                        345     #
    #                                      #
    # LEFT          ORIGIN           RIGHT #
    #                                      #
    #   165                        015     #
    #                                      #
    #      Q3                   Q4         #
    #                                      #
    #          105   DOWN   075            #
    ########################################

    if result >= 255 and result < 285:
        #print('UP')
        curr_status = 1

    elif result >= 285 and result < 345:
        #print('Q1')
        curr_status = 2

    elif result >= 345 and result < 360:
        #print('RIGHT')
        curr_status = 3

    elif result >= 0 and result < 15:
        #print('RIGHT')
        curr_status = 3

    elif result >= 15 and result < 75:
        #print('Q4')
        curr_status = 5

    elif result >= 75 and result < 105:
        #print('DOWN')
        curr_status = 6

    elif result >= 105 and result < 165:
        #print('Q3')
        curr_status = 7

    elif result >= 165 and result < 195:
        #print('LEFT')
        curr_status = 8

    elif result >= 195 and result < 255:
        #print('Q2')
        curr_status = 9

    if curr_status != prev_status:
        cv2.circle(image_frame, (x, y), 2, (255, 255, 0), 2)

        if x >= input_boundary[0] and x <= input_boundary[2] and y >= input_boundary[1] and y <= input_boundary[3]:
            # cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            point_queue.append((x, y))

    if len(point_queue) == 10:
        sum_x = 0
        sum_y = 0
        for i in point_queue:
            sum_x = sum_x + i[0]
            sum_y = sum_y + i[1]

        new_x = int(sum_x/len(point_queue))
        new_y = int(sum_y/len(point_queue))
        cv2.putText(image_frame, 'new input', (new_x - 15, new_y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255))
        cv2.circle(image_frame, (new_x, new_y), 2, (0, 0, 255), 2)
        cv2.rectangle(image_frame, (new_x - 70, new_y - 70), (new_x + 70, new_y + 70), (0, 255, 0), 2)
        input_boundary = [new_x-70,new_y-70,new_x+70,new_y+70]
        point_queue = []


def mouse_click(event, x, y, flags, param):
    global image_frame, is_first_click, count, prev, curr, boundary,input_boundary,center_input

    if is_first_click == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.putText(image_frame, 'input', (x - 15, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255))
            cv2.circle(image_frame, (x, y), 2, (0, 0, 255), 2)
            center_input = x,y
            #cv2.rectangle(image_frame,(x-70,y-70),(x+70,y+70),(0, 255, 0), 2)
            input_boundary = [x-70,y-70,x+70,y+70]
            is_first_click = 1

    elif is_first_click == 1:
        if event == cv2.EVENT_LBUTTONDOWN:
            prev = x, y
            curr = x, y
            boundary = [x - 15, y - 15, x + 15, y + 15]
            is_first_click = False
            is_first_click = 2

    elif is_first_click == 2:
        if x >= boundary[0] and x <= boundary[2] and y >= boundary[1] and y <= boundary[3]:
            pass
        else:
            boundary = [x - 15, y - 15, x + 15, y + 15]
            tracking(x, y)

    if event == cv2.EVENT_RBUTTONDOWN:
        image_frame = cv2.imread('../resources/images/black_background.png')
        is_first_click = 0

    #cv2.rectangle(image_frame, (boundary[0], boundary[1]), (boundary[2], boundary[3]), (0, 255, 0), 2)

if __name__ == "__main__":

    while True:
        cv2.imshow("Multiple color Detection", image_frame)
        cv2.setMouseCallback("Multiple color Detection", mouse_click)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
