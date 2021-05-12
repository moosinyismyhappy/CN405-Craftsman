import math

class GuiTracking():

    def __init__(self, gui, image_storage):
        self.gui = gui
        self.image_storage = image_storage
        self.previous_position = None
        self.current_position = None
        self.previous_direction = None
        self.current_direction = None
        self.center_boundary = None

    def degree(self, x):
        pi = math.pi
        degree = ((x * 180) / pi) % 360
        return int(degree)

    def set_center_boundary(self,new_boundary):
        self.center_boundary = new_boundary

    def get_center_boundary(self):
        return self.center_boundary

    def tracking_direction(self):
        pass

        ########################################
        #           Tracking Chart             #
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


