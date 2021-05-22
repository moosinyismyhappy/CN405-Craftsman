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

    def find_direction_degree(self,degree):
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

        if 250 <= degree < 290:
            return 1

        elif 290 <= degree < 340:
            return 2

        elif 340 <= degree < 360:
            return 3

        elif 0 <= degree < 20:
            return 3

        elif 20 <= degree < 70:
            return 4

        elif 70 <= degree < 110:
            return 5

        elif 110 <= degree < 160:
            return 6

        elif 160 <= degree < 200:
            return 7

        elif 200 <= degree < 250:
            return 8

    def find_average_point(self,list):
        sum_x = 0
        sum_y = 0
        for i in list:
            sum_x += i[0]
            sum_y += i[1]
        average_x = int(sum_x / len(list))
        average_y = int(sum_y / len(list))
        return average_x, average_y

    def find_max_min(self,list):
        min_x = list[0][0]
        min_y = list[0][1]
        max_x = list[0][0]
        max_y = list[0][1]
        for i in range(len(list)):
            if list[i][0] <= min_x:
                min_x = list[i][0]
            if list[i][0] >= max_x:
                max_x = list[i][0]
            if list[i][1] <= min_y:
                min_y = list[i][1]
            if list[i][1] >= max_y:
                max_y = list[i][1]
        return min_x, max_x, min_y, max_y

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
        direction_degree = self.degree(math.atan2(diff_y, diff_x))

        # Set current position to previous position for prepare new round
        self.previous_position = self.current_position

        # find direction from previous to current position
        self.current_direction = self.find_direction_degree(direction_degree)

        if self.current_direction != self.previous_direction:
            cv2.circle(self.image_storage.get_background_image_for_track(), center_position, 2, (0, 0, 255), 2)



