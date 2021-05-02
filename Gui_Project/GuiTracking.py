import math
import cv2


class GuiTracking():

    def __init__(self,gui,image_storage):
        self.gui = gui
        self.image_storage = image_storage
        self.current_center_position = None
        self.previous_center_position = None
        self.previous_position = None
        self.current_position = None
        self.previous_direction = None
        self.current_direction = None

    def set_center_position(self,new_center):
        self.current_center_position = new_center

    def print_center(self):
        print(self.current_center_position)
        #cv2.circle(self.image_storage.get_detected_image(), self.current_center_position, 2, (0, 0, 255), 2)

    def degree(self,x):
        pi = math.pi
        degree = ((x * 180) / pi) % 360
        return int(degree)

    """def tracking_direction(self):

        ########################################
        #           Tracking Chart             #
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

        prev_right = curr_right
        curr_right = x, y
        prev_status_right = curr_status_right

        diff_x = curr_right[0] - prev_right[0]
        diff_y = curr_right[1] - prev_right[1]

        result = degree(math.atan2(diff_y, diff_x))

        if result >= 240 and result < 300:
            print('UP')
            curr_status_right = 1

        elif result >= 300 and result < 330:
            print('Q1')
            curr_status_right = 2

        elif result >= 330 and result < 360:
            print('RIGHT')
            curr_status_right = 3

        elif result >= 0 and result < 30:
            print('RIGHT')
            curr_status_right = 4

        elif result >= 30 and result < 60:
            print('Q4')
            curr_status_right = 5

        elif result >= 60 and result < 120:
            print('DOWN')
            curr_status_right = 6

        elif result >= 120 and result < 150:
            print('Q3')
            curr_status_right = 7

        elif result >= 150 and result < 210:
            print('LEFT')
            curr_status_right = 8

        elif result >= 210 and result < 240:
            print('Q2')
            curr_status_right = 9

        if curr_status_right != prev_status_right:
            cv2.circle(black_img, (x, y), 2, (0, 255, 255), 2)"""

