import threading
import time


class GuiTimer(threading.Thread):

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.value_for_calibrate = self.gui.get_reference_value_for_calibrate()
        self.layout = self.gui.get_reference_layout()

        # input1 timer
        self.input1_start_time = 0
        self.input1_end_time = 0
        self.input1_total_time = 0
        self.input1_timer_status = -1
        self.input1_is_pass_interested_area = False

        # input2 timer
        self.input2_start_time = 0
        self.input2_end_time = 0
        self.input2_total_time = 0
        self.input2_timer_status = -1
        self.input2_is_pass_interested_area = False

        # output timer
        self.output_start_time = 0
        self.output_end_time = 0
        self.output_total_time = 0
        self.output_timer_status = -1
        self.output_is_pass_interested_area = False

        # work timer
        self.work_start_time = 0
        self.work_end_time = 0
        self.work_total_time = 0
        self.work_timer_status = -1

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        self.calculate_time()

    def calculate_time(self):
        while True:

            # for this loop can run without lag (unknown cause)
            time.sleep(0)

            # timer button is start
            if self.value_for_calibrate.get_timer_ready_status() is True:

                # timer status = -1 : disable
                # timer status = 0 : standby
                # timer status = 1 : start
                # timer status = 2 : continue record time

                current_area_left = self.value_for_calibrate.get_current_area_left()
                current_area_right = self.value_for_calibrate.get_current_area_right()

                # input1 timer
                # start from work area
                if current_area_left == 4:
                    # first time : enable timer
                    if self.input1_timer_status == -1:
                        # set timer to standby
                        self.input1_timer_status = 0

                    elif self.input1_is_pass_interested_area is True and self.input1_timer_status == 2:
                        # disable timer and calculate used time
                        self.input1_timer_status = -1
                        self.input1_is_pass_interested_area = False
                        # stamp end time
                        self.input1_end_time = time.time()
                        self.input1_total_time = round((self.input1_end_time - self.input1_start_time), 2)

                        # display time to gui with x:xx format
                        text_input1_total_time = str(self.input1_total_time)
                        text_input1_total_time = text_input1_total_time.split('.')

                        # add one digit at last if there is only one digit to display
                        if len(text_input1_total_time[1]) == 1:
                            text_input1_total_time[1] = text_input1_total_time[1] + '0'

                        text_input1_total_time = text_input1_total_time[0] + ':' + text_input1_total_time[1]
                        self.layout.text_display_avg_input1.setText(str(text_input1_total_time))
                        # print('Input1 Time:', self.input1_total_time, 'seconds')

                # center out of work area and timer is standby
                elif current_area_left == -1 and self.input1_timer_status == 0:
                    # set timer to start
                    self.input1_timer_status = 1
                    # stamp start time
                    self.input1_start_time = time.time()

                # once timer start still catch time until timer stop
                elif current_area_left == -1 and self.input1_timer_status == 1:
                    self.input1_timer_status = 2

                # center is in input1 area once
                if current_area_left == 1:
                    self.input1_is_pass_interested_area = True

                #########################################################

                # input2 timer
                # start from output area
                if current_area_right == 3:
                    # first time : enable timer
                    if self.input2_timer_status == -1:
                        # set timer to standby
                        self.input2_timer_status = 0

                # center out of output area and timer is standby
                elif current_area_right == -1 and self.input2_timer_status == 0:
                    # set timer to start
                    self.input2_timer_status = 1
                    # stamp start time
                    self.input2_start_time = time.time()


                # once timer start still catch time until timer stop
                elif current_area_right == -1 and self.input2_timer_status == 1:
                    self.input2_timer_status = 2

                # center is in input2 area once
                if current_area_right == 2:
                    self.input2_is_pass_interested_area = True

                # center is in work area with timer start and already pass input2 area
                elif current_area_right == 4 and self.input2_timer_status == 2 and self.input2_is_pass_interested_area is True:
                    # disable timer and calculate used time
                    self.input2_timer_status = -1
                    self.input2_is_pass_interested_area = False
                    # stamp end time
                    self.input2_end_time = time.time()
                    self.input2_total_time = round((self.input2_end_time - self.input2_start_time), 2)

                    # display time to gui with x:xx format
                    text_input2_total_time = str(self.input2_total_time)
                    text_input2_total_time = text_input2_total_time.split('.')

                    # add one digit at last if there is only one digit to display
                    if len(text_input2_total_time[1]) == 1:
                        text_input2_total_time[1] = text_input2_total_time[1] + '0'

                    text_input2_total_time = text_input2_total_time[0] + ':' + text_input2_total_time[1]
                    self.layout.text_display_avg_input2.setText(str(text_input2_total_time))
                    # print('Input2 Time:', self.input2_total_time, 'seconds')

                #########################################################

                # output timer
                # start from work area
                if current_area_right == 4:
                    # first time : enable timer
                    if self.output_timer_status == -1:
                        # set timer to standby
                        self.output_timer_status = 0

                # center out of work area and timer is standby
                elif current_area_right == -1 and self.output_timer_status == 0:
                    # set timer to start
                    self.output_timer_status = 1
                    # stamp start time
                    self.output_start_time = time.time()


                # once timer start still catch time until timer stop
                elif current_area_right == -1 and self.output_timer_status == 1:
                    self.output_timer_status = 2

                # center is in output area once
                if current_area_right == 3:
                    self.output_is_pass_interested_area = True

                # center is out of output area. stop timer and calculate used time
                elif current_area_right == -1 and self.output_timer_status == 2 and self.output_is_pass_interested_area is True:
                    # disable timer
                    self.output_timer_status = -1
                    self.output_is_pass_interested_area = False
                    # stamp end time
                    self.output_end_time = time.time()

                    # this case use for fix bug (unknown cause)
                    if (self.output_end_time - self.output_start_time) == 0:
                        # set timer to standby
                        self.output_timer_status = 0
                    else:
                        self.output_total_time = round((self.output_end_time - self.output_start_time), 2)

                        # display time to gui with x:xx format
                        text_output_total_time = str(self.output_total_time)
                        text_output_total_time = text_output_total_time.split('.')

                        # add one digit at last if there is only one digit to display
                        if len(text_output_total_time[1]) == 1:
                            text_output_total_time[1] = text_output_total_time[1] + '0'

                        text_output_total_time = text_output_total_time[0] + ':' + text_output_total_time[1]
                        self.layout.text_display_avg_output.setText(str(text_output_total_time))
                        # print('Output Time:', self.output_total_time, 'seconds')

                #########################################################

                # work timer
                # start from work area
                if current_area_left == 4 and current_area_right == 4:
                    # first time : enable timer
                    if self.work_timer_status == -1:
                        # set timer to start
                        self.work_timer_status = 1
                        # stamp start time
                        self.work_start_time = time.time()

                    # once timer start still catch time until timer stop
                    elif self.work_timer_status == 1:
                        self.work_timer_status = 2

                # center is out of work area. stop timer and calculate used time
                elif self.work_timer_status == 2:
                    # disable timer
                    self.work_timer_status = -1
                    # stamp end time
                    self.work_end_time = time.time()
                    self.work_total_time = round((self.work_end_time - self.work_start_time), 2)

                    # display time to gui with x:xx format
                    text_work_total_time = str(self.work_total_time)
                    text_work_total_time = text_work_total_time.split('.')

                    # add one digit at last if there is only one digit to display
                    if len(text_work_total_time[1]) == 1:
                        text_work_total_time[1] = text_work_total_time[1] + '0'

                    text_work_total_time = text_work_total_time[0] + ':' + text_work_total_time[1]
                    self.layout.text_display_avg_work.setText(str(text_work_total_time))
                    # print('Work Time:', self.work_total_time, 'seconds')
