import math
import cv2


class GuiTracking():

    def __init__(self, gui, image_storage,color_detect):
        self.gui = gui
        self.image_storage = image_storage
        self.color_detect = color_detect
        self.previous_position = None
        self.current_position = None
        self.previous_direction = None
        self.current_direction = None
        self.center_boundary = None
        self.is_position_out_of_boundary = False

    # set current position
    def set_current_position(self, new_position):
        self.current_position = new_position

    # get current position
    def get_current_position(self):
        return self.current_position

    # set previous position
    def set_previous_position(self, new_position):
        self.previous_position = new_position

    # get previous position
    def get_previous_position(self):
        return self.previous_position

    # set current direction
    def set_current_direction(self, new_direction):
        self.current_direction = new_direction

    # get current direction
    def get_current_direction(self):
        return self.current_direction

    # set previous direction
    def set_previous_direction(self, new_direction):
        self.previous_direction = new_direction

    # get previous direction
    def get_previous_direction(self):
        return self.previous_direction

    def set_center_boundary(self, new_boundary):
        self.center_boundary = new_boundary

    def get_center_boundary(self):
        return self.center_boundary

    def set_is_position_out_of_boundary(self,new_status):
        self.is_position_out_of_boundary = new_status

    def get_is_position_out_of_boundary(self):
        return self.is_position_out_of_boundary

    # Convert radian to degree
    def degree(self, x):
        pi = math.pi
        degree = ((x * 180) / pi) % 360
        return int(degree)

    # check center is in rectangle boundary
    def is_center_in_boundary(self, center_position):
        x_center, y_center = center_position[0], center_position[1]
        # boundary of rectangle
        x1 = self.get_center_boundary()[0]
        y1 = self.get_center_boundary()[1]
        x2 = self.get_center_boundary()[2]
        y2 = self.get_center_boundary()[3]
        if x_center >= x1 and x_center <= x2 and y_center >= y1 and y_center <= y2:
            self.set_is_position_out_of_boundary(False)
        else:
            self.__tracking_direction(center_position)
            self.set_is_position_out_of_boundary(True)

    # set to private method for is_out_of_boundary call in class
    def __tracking_direction(self,center_position):
        self.current_position = center_position
        self.previous_direction = self.current_direction

        diff_x = self.current_position[0] - self.previous_position[0]
        diff_y = self.current_position[1] - self.previous_position[1]
        result = self.degree(math.atan2(diff_y, diff_x))

        # Set current position to previous position for prepare new round
        self.previous_position = self.current_position

        ########################################
        #           Tracking Chart             #
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
            self.current_direction = 1

        elif result >= 290 and result < 340:
            # print('Q1')
            self.current_direction = 2

        elif result >= 340 and result < 360:
            # print('RIGHT')
            self.current_direction = 3

        elif result >= 0 and result < 20:
            # print('RIGHT')
            self.current_direction = 3

        elif result >= 20 and result < 70:
            # print('Q4')
            self.current_direction = 5

        elif result >= 70 and result < 110:
            # print('DOWN')
            self.current_direction = 6

        elif result >= 110 and result < 160:
            # print('Q3')
            self.current_direction = 7

        elif result >= 160 and result < 200:
            # print('LEFT')
            self.current_direction = 8

        elif result >= 200 and result < 250:
            # print('Q2')
            self.current_direction = 9

        if self.current_direction != self.previous_direction:
            cv2.circle(self.image_storage.get_background_image_for_track(), center_position, 2, (0, 0, 255), 2)



