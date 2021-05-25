class GuiCalibrate:

    def __init__(self):
        self.input1_list = []
        self.input2_list = []
        self.output_list = []
        self.work_list = []
        self.rectangle_list = []

        self.calibrate_area_status = True

        self.input1_calibrate_status = True
        self.input2_calibrate_status = True
        self.output_calibrate_status = True
        self.work_calibrate_status = True

        self.display_input1_area_status = False
        self.display_input2_area_status = False
        self.display_output_area_status = False
        self.display_work_area_status = False

        self.input1_calibrate_area = [-1, -1, -1, -1]
        self.input2_calibrate_area = [-1, -1, -1, -1]
        self.output_calibrate_area = [-1, -1, -1, -1]
        self.work_calibrate_area = [-1, -1, -1, -1]

        self.center_point_boundary = None
        self.is_position_out_of_boundary = False
        self.minimum_distance = 100

    def set_input1_list(self, new_list):
        self.input1_list = new_list

    def get_input1_list(self):
        return self.input1_list

    def set_input2_list(self, new_list):
        self.input2_list = new_list

    def get_input2_list(self):
        return self.input2_list

    def set_output_list(self, new_list):
        self.input1_list = new_list

    def get_output_list(self):
        return self.output_list

    def set_work_list(self, new_list):
        self.input1_list = new_list

    def get_work_list(self):
        return self.work_list

    def set_rectangle_list(self, new_list):
        self.rectangle_list = new_list

    def get_rectangle_list(self):
        return self.rectangle_list

    def set_calibrate_area_status(self, new_status):
        self.calibrate_area_status = new_status

    def get_calibrate_area_status(self):
        return self.calibrate_area_status

    def set_input1_calibrate_status(self, new_status):
        self.input1_calibrate_status = new_status

    def get_input1_calibrate_status(self):
        return self.input1_calibrate_status

    def set_input2_calibrate_status(self, new_status):
        self.input2_calibrate_status = new_status

    def get_input2_calibrate_status(self):
        return self.input2_calibrate_status

    def set_output_calibrate_status(self, new_status):
        self.output_calibrate_status = new_status

    def get_output_calibrate_status(self):
        return self.output_calibrate_status

    def set_work_calibrate_status(self, new_status):
        self.work_calibrate_status = new_status

    def get_work_calibrate_status(self):
        return self.work_calibrate_status

    def set_display_input1_area_status(self, new_status):
        self.display_input1_area_status = new_status

    def get_display_input1_area_status(self):
        return self.display_input1_area_status

    def set_display_input2_area_status(self, new_status):
        self.display_input2_area_status = new_status

    def get_display_input2_area_status(self):
        return self.display_input2_area_status

    def set_display_output_area_status(self, new_status):
        self.display_output_area_status = new_status

    def get_display_output_area_status(self):
        return self.display_output_area_status

    def set_display_work_area_status(self, new_status):
        self.display_work_area_status = new_status

    def get_display_work_area_status(self):
        return self.display_work_area_status

    def set_input1_calibrate_area(self, new_area):
        self.input1_calibrate_area = new_area

    def get_input1_calibrate_area(self):
        return self.input1_calibrate_area

    def set_input2_calibrate_area(self, new_area):
        self.input2_calibrate_area = new_area

    def get_input2_calibrate_area(self):
        return self.input2_calibrate_area

    def set_output_calibrate_area(self, new_area):
        self.output_calibrate_area = new_area

    def get_output_calibrate_area(self):
        return self.output_calibrate_area

    def set_work_calibrate_area(self, new_area):
        self.work_calibrate_area = new_area

    def get_work_calibrate_area(self):
        return self.work_calibrate_area

    def set_center_point_boundary(self,new_boundary):
        self.center_point_boundary = new_boundary

    def get_center_point_boundary(self):
        return self.center_point_boundary

    def set_is_position_out_of_boundary(self,new_status):
        self.is_position_out_of_boundary = new_status

    def get_is_position_out_of_boundary(self):
        return self.is_position_out_of_boundary

    def set_minimum_distance(self,new_distance):
        self.minimum_distance = new_distance

    def get_minimum_distance(self):
        return self.minimum_distance
