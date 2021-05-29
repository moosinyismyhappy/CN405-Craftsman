import threading
import time


class GuiTimer(threading.Thread):

    def __init__(self,gui):
        super().__init__()
        self.gui = gui
        self.calibrate = self.gui.get_reference_calibrate()
        self.layout = self.gui.get_reference_layout()
        self.work_time_now = 0
        self.work_time_end = 0

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        #self.calculate_time()

    def calculate_time(self):
        pass
