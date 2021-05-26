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
        self.calculate_time()

    def calculate_time(self):
        while True:

            print(self.calibrate.get_work_area_counter())

            """if self.calibrate.get_work_area_counter == 0:
                self.work_time_now = time.time()

            if self.calibrate.get_work_area_counter == 2:
                self.work_time_end = time.time()

            total_work_time = self.work_time_end - self.work_time_now
            self.layout.text_display_avg_work.setText(str(total_work_time))
            print(total_work_time)"""
