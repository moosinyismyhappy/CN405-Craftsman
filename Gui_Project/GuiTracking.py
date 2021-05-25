import math
import cv2


class GuiTracking():

    def __init__(self, gui, image_storage, color_detect):
        self.gui = gui
        self.image_storage = image_storage
        self.color_detect = color_detect
        self.calibrate = self.gui.get_reference_calibrate()

        # center point
        self.prev_position = -1
        self.curr_position = -1
        self.prev_direction = -1
        self.curr_direction = -1

        # distance
        self.prev_distance_input1 = -1
        self.prev_distance_input2 = -1
        self.prev_distance_output = -1
        self.prev_distance_work = -1
        self.curr_distance_input1 = -1
        self.curr_distance_input2 = -1
        self.curr_distance_output = -1
        self.curr_distance_work = -1

        # direction
        self.prev_direction_input1 = -1
        self.prev_direction_input2 = -1
        self.prev_direction_output = -1
        self.prev_direction_work = -1
        self.curr_direction_input1 = -1
        self.curr_direction_input2 = -1
        self.curr_direction_output = -1
        self.curr_direction_work = -1

        # counter
        self.count_approaching_input1 = 0
        self.count_approaching_input2 = 0
        self.count_approaching_output = 0
        self.count_approaching_work = 0

    def find_direction_number(self, degree):
        ########################################
        #          260    UP    280            #
        #                                      #
        #      Q2                   Q1         #
        #                                      #
        #   190                        350     #
        #                                      #
        # LEFT          ORIGIN           RIGHT #
        #                                      #
        #   170                        010     #
        #                                      #
        #      Q3                   Q4         #
        #                                      #
        #          100   DOWN   80             #
        ########################################
        if 260 <= degree < 280:
            return 1
        elif 280 <= degree < 350:
            return 2
        elif 350 <= degree < 360:
            return 3
        elif 0 <= degree < 10:
            return 3
        elif 10 <= degree < 80:
            return 4
        elif 80 <= degree < 100:
            return 5
        elif 100 <= degree < 170:
            return 6
        elif 170 <= degree < 190:
            return 7
        elif 190 <= degree < 260:
            return 8

    def find_average_point(self, list):
        sum_x = 0
        sum_y = 0
        for i in list:
            sum_x += i[0]
            sum_y += i[1]
        average_x = int(sum_x / len(list))
        average_y = int(sum_y / len(list))
        return average_x, average_y

    def find_max_min(self, list):
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

    def process_rectangle(self, list):
        min_x, max_x, min_y, max_y = self.find_max_min(list)
        return min_x, min_y, max_x, max_y

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

    def set_center_point_boundary(self, new_boundary):
        x1 = new_boundary[0] + self.gui.get_dial_center_point_boundary()
        y1 = new_boundary[1] + self.gui.get_dial_center_point_boundary()
        x2 = new_boundary[2] - self.gui.get_dial_center_point_boundary()
        y2 = new_boundary[3] - self.gui.get_dial_center_point_boundary()
        self.center_point_boundary = [x1, y1, x2, y2]

    def get_center_point_boundary(self):
        return self.center_point_boundary

    def set_is_position_out_of_boundary(self, new_status):
        self.is_position_out_of_boundary = new_status

    def get_is_position_out_of_boundary(self):
        return self.is_position_out_of_boundary

    def calculate_distance(self, origin, points):
        return int(math.sqrt(((points[0] - origin[0]) ** 2) + ((points[1] - origin[1]) ** 2)))

    def calculate_degree(self, x):
        pi = math.pi
        degree = ((x * 180) / pi) % 360
        return int(degree)

    # check center is in rectangle boundary
    def is_center_point_in_boundary(self, center_position):
        x_center, y_center = center_position[0], center_position[1]
        # center point boundary
        x1 = self.get_center_point_boundary()[0]
        y1 = self.get_center_point_boundary()[1]
        x2 = self.get_center_point_boundary()[2]
        y2 = self.get_center_point_boundary()[3]
        if x1 <= x_center <= x2 and y1 <= y_center <= y2:
            self.set_is_position_out_of_boundary(False)
        else:
            self.__tracking_direction(center_position)
            self.set_is_position_out_of_boundary(True)

    # set to private method for is_out_of_boundary call in class
    def __tracking_direction(self, center_position):
        # set current position and direction to previous, setup for next round
        self.previous_position = self.current_position
        self.previous_direction = self.current_direction
        self.current_position = center_position

        # calculate difference between current point and previous point
        diff_x = self.current_position[0] - self.previous_position[0]
        diff_y = self.current_position[1] - self.previous_position[1]

        # set current distance to previous
        self.prev_distance_input1 = self.curr_distance_input1
        self.prev_distance_input2 = self.curr_distance_input2
        self.prev_distance_output = self.curr_distance_output
        self.prev_distance_work = self.curr_distance_work

        # set current direction to previous
        self.prev_direction_input1 = self.curr_direction_input1
        self.prev_direction_input2 = self.curr_direction_input2
        self.prev_direction_output = self.curr_direction_output
        self.prev_direction_work = self.curr_direction_work

        # temp variable
        # Calculate direction from previous to current point
        point_direction_degree = self.calculate_degree(math.atan2(diff_y, diff_x))

        # temp variable
        # Calculate direction from current point to all area
        x = center_position[0]
        y = center_position[1]

        # reassign input1 to short due to long command to get value from GuiController
        input1_position = self.gui.get_input1_position()
        input2_position = self.gui.get_input2_position()
        output_position = self.gui.get_output_position()
        work_position = self.gui.get_work_position()

        direction_input1_degree = self.calculate_degree(
            math.atan2(input1_position[1] - y, input1_position[0] - x))
        direction_input2_degree = self.calculate_degree(
            math.atan2(input2_position[1] - y, input2_position[0] - x))
        direction_output_degree = self.calculate_degree(
            math.atan2(output_position[1] - y, output_position[0] - x))
        direction_work_degree = self.calculate_degree(math.atan2(work_position[1] - y, work_position[0] - x))

        # Calculate distance from current point to all area
        self.curr_distance_input1 = self.calculate_distance(input1_position, (x, y))
        self.curr_distance_input2 = self.calculate_distance(input2_position, (x, y))
        self.curr_distance_output = self.calculate_distance(output_position, (x, y))
        self.curr_distance_work = self.calculate_distance(work_position, (x, y))

        # find direction number
        self.curr_direction = self.find_direction_number(point_direction_degree)
        self.curr_direction_input1 = self.find_direction_number(direction_input1_degree)
        self.curr_direction_input2 = self.find_direction_number(direction_input2_degree)
        self.curr_direction_output = self.find_direction_number(direction_output_degree)
        self.curr_direction_work = self.find_direction_number(direction_work_degree)

        # increase counter when approaching area with lower distance and not change direction
        # except work area due to many direction to approaching. it's use only distance
        if self.prev_distance_input1 > self.curr_distance_input1 and self.curr_direction_input1 == self.curr_direction:
            self.count_approaching_input1 += 1

        if self.prev_distance_input2 > self.curr_distance_input2 and self.curr_direction_input2 == self.curr_direction:
            self.count_approaching_input2 += 1

        if self.prev_distance_output > self.curr_distance_output and self.curr_direction_output == self.curr_direction:
            self.count_approaching_output += 1

        # do this when direction is changed
        if self.curr_direction != self.prev_direction:

            # temp variable
            # get background image to draw points
            background_image = self.image_storage.get_background_image_for_track()
            # create temp list to keep counter and find index that has maximum counter that mean maximum approach
            max_approaching_list = [self.count_approaching_input1, self.count_approaching_input2,
                                    self.count_approaching_output]
            max_approaching = max_approaching_list.index(max(max_approaching_list))

            # approached input1
            if max_approaching == 0:
                if self.curr_distance_input1 < self.minimum_distance:
                    cv2.circle(background_image, (x, y), 2, (0, 0, 255), 2)
                    cv2.putText(background_image, str((x, y, 'Input1')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.3, (0, 0, 255))
                    if self.calibrate_area_status:
                        if self.input1_calibrate_status:
                            self.input1_list.append((x, y))
                            self.gui.display_calibrated_number_input1(len(self.input1_list))

            # approached input2
            elif max_approaching == 1:
                if self.curr_distance_input2 < self.minimum_distance:
                    cv2.circle(background_image, (x, y), 2, (0, 150, 255), 2)
                    cv2.putText(background_image, str((x, y, 'Input2')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.3, (0, 150, 255))
                    if self.calibrate_area_status:
                        if self.input2_calibrate_status:
                            self.input2_list.append((x, y))
                            self.gui.display_calibrated_number_input2(len(self.input2_list))

            # approached output
            elif max_approaching == 2:
                if self.curr_distance_output < self.minimum_distance:
                    cv2.circle(background_image, (x, y), 2, (0, 80, 255), 2)
                    cv2.putText(background_image, str((x, y, 'Output')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.3, (0, 80, 255))
                    if self.calibrate_area_status:
                        if self.output_calibrate_status:
                            self.output_list.append((x, y))
                            self.gui.display_calibrated_number_output(len(self.output_list))

            if self.curr_distance_work < self.minimum_distance:
                cv2.circle(background_image, (x, y), 2, (150, 80, 255), 2)
                cv2.putText(background_image, str((x, y, 'Work')), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (150, 80, 255))
                if self.calibrate_area_status:
                    if self.work_calibrate_status:
                        self.work_list.append((x, y))
                        self.gui.display_calibrated_number_work(len(self.work_list))

            # reset approach counter after change direction
            self.count_approaching_input1_left = 0
            self.count_approaching_input2_left = 0
            self.count_approaching_output_left = 0
            self.count_approaching_work_left = 0

        if len(self.input1_list) == self.gui.get_input1_calibrate_time():
            # process boundary of rectangle
            x1, y1, x2, y2 = self.process_rectangle(self.input1_list)

            # keep area of rectangle
            self.input1_calibrate_area = [x1, y1, x2, y2]

            # stop calibrate and clear list
            self.input1_calibrate_status = False
            self.input1_list.clear()

            # enable display area
            self.display_input1_area = True

        if len(self.input2_list) == self.gui.get_input2_calibrate_time():
            # process boundary of rectangle
            x1, y1, x2, y2 = self.process_rectangle(self.input2_list)

            # keep area of rectangle
            self.input2_calibrate_area = [x1, y1, x2, y2]

            # stop calibrate and clear list
            self.input2_calibrate_status = False
            self.input2_list.clear()

            # enable display area
            self.display_input2_area = True

        if len(self.output_list) == self.gui.get_output_calibrate_time():
            # process boundary of rectangle
            x1, y1, x2, y2 = self.process_rectangle(self.output_list)

            # keep area of rectangle
            self.output_calibrate_area = [x1, y1, x2, y2]

            # stop calibrate and clear list
            self.output_calibrate_status = False
            self.output_list.clear()

            # enable display area
            self.display_output_area = True

        if len(self.work_list) == self.gui.get_work_calibrate_time():
            # process boundary of rectangle
            x1, y1, x2, y2 = self.process_rectangle(self.work_list)

            # keep area of rectangle
            self.work_calibrate_area = [x1, y1, x2, y2]

            # stop calibrate and clear list
            self.work_calibrate_status = False
            self.work_list.clear()

            # enable display area
            self.display_work_area = True

    def is_rectangle_overlap(self, rect1, rect2):
        if (rect1[0] >= rect2[2]) or (rect1[2] <= rect2[0]) or (rect1[3] <= rect2[1]) or (rect1[1] >= rect2[3]):
            # no overlap occur
            return False
        else:
            # overlap occur
            return True

    def where_rectangle_overlap(self, rect1, rect2):
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
            raise Exception('No solution for overlap inside other rectangle')
        # overlap outside other rectangle
        elif x1 < u1 < u2 and y1 < v1 < v2 and u1 < u2 < x2 and v1 < v2 < y2:
            raise Exception('No solution for overlap outside other rectangle')

    def overlap_resolution(self, overlap_status, reference_rect, rect):

        self.x1 = rect[0]
        self.y1 = rect[1]
        self.x2 = rect[2]
        self.y2 = rect[3]

        if overlap_status == 0:
            self.x2 = reference_rect[0] - 1
        elif overlap_status == 1:
            self.x1 = reference_rect[2] + 1
        elif overlap_status == 2:
            self.y2 = reference_rect[1] - 1
        elif overlap_status == 3:
            self.y1 = reference_rect[3] + 1

        elif overlap_status == 4:
            if self.x2 - self.x1 > self.y2 - self.y1:
                self.x2 = reference_rect[0] - 1
            else:
                self.y2 = reference_rect[1] - 1
        elif overlap_status == 5:
            if self.x2 - self.x1 > self.y2 - self.y1:
                self.x1 = reference_rect[2] + 1
            else:
                self.y2 = reference_rect[1] - 1
        elif overlap_status == 6:
            if self.x2 - self.x1 > self.y2 - self.y1:
                self.x2 = reference_rect[0] - 1
            else:
                self.y1 = reference_rect[3] + 1
        elif overlap_status == 7:
            if self.x2 - self.x1 > self.y2 - self.y1:
                self.x1 = reference_rect[2] - 1
            else:
                self.y1 = reference_rect[3] + 1

        elif overlap_status == 8:
            self.x2 = reference_rect[0] - 1
        elif overlap_status == 9:
            raise Exception('No solution. Recalibrate ...')
        elif overlap_status == 10:
            self.x1 = reference_rect[2] + 1

        elif overlap_status == 11:
            self.y2 = reference_rect[1] - 1
        elif overlap_status == 12:
            raise Exception('No solution. Recalibrate ...')
        elif overlap_status == 13:
            self.y1 = reference_rect[3] + 1

        elif overlap_status == 14:
            raise Exception('No solution. Recalibrate ...')
        elif overlap_status == 15:
            raise Exception('No solution. Recalibrate ...')
