import threading
from threading import Thread


class GuiColorDetection(Thread):

    def __init__(self, gui, input_storage):
        super().__init__()
        self.gui = gui
        self.image_storage = input_storage
        self.x = -1
        self.y = -1
        self.hsv_range = 0.2
        self.hsv_list = None

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.detect_color()

    def __hsv_upper_process(self):
        h_upper = int(self.hsv_list[0] * (1 + self.hsv_range))
        s_upper = int(self.hsv_list[1] * (1 + self.hsv_range))
        v_upper = int(self.hsv_list[2] * (1 + self.hsv_range))

        # Set limit maximum of hsv value not more than 255
        if h_upper >= 255: h_upper = 255
        if s_upper >= 255: s_upper = 255
        if v_upper >= 255: v_upper = 255

        # combine hsv separate value to list
        self.hsv_upper = [h_upper, s_upper, v_upper]

    def __hsv_lower_process(self):
        h_lower = int(self.hsv_list[0] * (1 - self.hsv_range))
        s_lower = int(self.hsv_list[1] * (1 - self.hsv_range))
        v_lower = int(self.hsv_list[2] * (1 - self.hsv_range))

        # Set limit minimum of hsv value not more than 255
        if h_lower >= 255: h_lower = 255
        if s_lower >= 255: s_lower = 255
        if v_lower >= 255: v_lower = 255

        # combine hsv separate value to list
        self.hsv_lower = [h_lower, s_lower, v_lower]

    def set_hsv(self):
        pass

    def detect_color(self):
        print('Detecting color ...')

    def print_hsv_value(self):
        print(self.image_storage.get_hsv_image()[self.y, self.x])

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y
