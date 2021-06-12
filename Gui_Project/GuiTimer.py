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
        self.input1_in_round_time = 0
        self.input1_counter = 0
        self.input1_timer_status = -1
        self.input1_is_pass_interested_area = False

        # input2 timer
        self.input2_start_time = 0
        self.input2_end_time = 0
        self.input2_total_time = 0
        self.input2_in_round_time = 0
        self.input2_counter = 0
        self.input2_timer_status = -1
        self.input2_is_pass_interested_area = False

        # output timer
        self.output_start_time = 0
        self.output_end_time = 0
        self.output_total_time = 0
        self.output_in_round_time = 0
        self.output_counter = 0
        self.output_timer_status = -1
        self.output_is_pass_interested_area = False

        # work timer
        self.work_start_time = 0
        self.work_end_time = 0
        self.work_total_time = 0
        self.work_in_round_time = 0
        self.work_counter = 0
        self.work_timer_status = -1

        # cycle timer
        self.cycle_start_time = 0
        self.cycle_end_time = 0
        self.cycle_total_time = 0
        self.cycle_in_round_time = 0
        self.cycle_counter = 0
        self.cycle_timer_status = -1
        self.cycle_is_pass_interested_area = False

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
                        self.input1_in_round_time = round((self.input1_end_time - self.input1_start_time), 2)
                        # add in round time to total time and increase counter by 1 for finish round
                        self.input1_total_time = self.input1_total_time + self.input1_in_round_time
                        self.input1_counter = self.input1_counter + 1

                        # display time to gui
                        # at first round if counter is 0 it will divide by zero so error will occur
                        # display average input1 time
                        if self.input1_counter != 0:
                            input1_average_time = self.input1_total_time / self.input1_counter
                            input1_average_time = round(input1_average_time, 2)
                            self.layout.text_display_input1_avg_time.setText(str(input1_average_time))
                        # display in-round time
                        self.layout.text_display_input1_time.setText(str(self.input1_in_round_time))


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
                    self.input2_in_round_time = round((self.input2_end_time - self.input2_start_time), 2)
                    # add in round time to total time and increase counter by 1 for finish round
                    self.input2_total_time = self.input2_total_time + self.input2_in_round_time
                    self.input2_counter = self.input2_counter + 1

                    # display time to gui
                    # at first round if counter is 0 it will divide by zero so error will occur
                    # display average input2 time
                    if self.input2_counter != 0:
                        input2_average_time = self.input2_total_time / self.input2_counter
                        input2_average_time = round(input2_average_time, 2)
                        self.layout.text_display_input2_avg_time.setText(str(input2_average_time))
                    # display in-round time
                    self.layout.text_display_input2_time.setText(str(self.input2_in_round_time))

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
                        self.output_in_round_time = round((self.output_end_time - self.output_start_time), 2)
                        # add in round time to total time and increase counter by 1 for finish round
                        self.output_total_time = self.output_total_time + self.output_in_round_time
                        self.output_counter = self.output_counter + 1

                        # display time to gui
                        # at first round if counter is 0 it will divide by zero so error will occur
                        # display average output time
                        if self.output_counter != 0:
                            output_average_time = self.output_total_time / self.output_counter
                            output_average_time = round(output_average_time, 2)
                            self.layout.text_display_output_avg_time.setText(str(output_average_time))
                        # display in-round time
                        self.layout.text_display_output_time.setText(str(self.output_in_round_time))

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
                    self.work_in_round_time = round((self.work_end_time - self.work_start_time), 2)
                    # add in round time to total time and increase counter by 1 for finish round
                    self.work_total_time = self.work_total_time + self.work_in_round_time
                    self.work_counter = self.work_counter + 1

                    # display time to gui
                    # at first round if counter is 0 it will divide by zero so error will occur
                    # display average work time
                    if self.work_counter != 0:
                        work_average_time = self.work_total_time / self.work_counter
                        work_average_time = round(work_average_time, 2)
                        self.layout.text_display_work_avg_time.setText(str(work_average_time))
                    # display in-round time
                    self.layout.text_display_work_time.setText(str(self.work_in_round_time))

                #########################################################

                # cycle timer
                # start from output area
                if current_area_right == 3:
                    # first time : enable timer
                    if self.cycle_timer_status == -1:
                        # set timer to standby
                        self.cycle_timer_status = 0

                    # center is back to output area with started timer and pass work area
                    # stop timer and calculate used time
                    elif self.cycle_timer_status == 2 and self.cycle_is_pass_interested_area is True:
                        # reset timer and passed area
                        self.cycle_timer_status = -1
                        self.cycle_is_pass_interested_area = False
                        # stamp end time
                        self.cycle_end_time = time.time()
                        self.cycle_in_round_time = round((self.cycle_end_time - self.cycle_start_time), 2)
                        # add in round time to total time and increase counter by 1 for finish round
                        self.cycle_total_time = self.cycle_total_time + self.cycle_in_round_time
                        self.cycle_counter = self.cycle_counter + 1

                        # display time to gui
                        # at first round if counter is 0 it will divide by zero so error will occur
                        # display average cycle time
                        if self.cycle_counter != 0:
                            cycle_average_time = self.cycle_total_time / self.cycle_counter
                            cycle_average_time = round(cycle_average_time, 2)
                            self.layout.text_display_cycle_avg_time.setText(str(cycle_average_time))
                        # display in-round time
                        self.layout.text_display_cycle_time.setText(str(self.cycle_in_round_time))

                # center out of output with standby timer so it will start timer
                elif current_area_right == -1 and self.cycle_timer_status == 0:
                    # set timer to start
                    self.cycle_timer_status = 1
                    # stamp start time
                    self.cycle_start_time = time.time()

                # once timer start still catch time until timer stop
                elif current_area_right == -1 and self.cycle_timer_status == 1:
                    self.cycle_timer_status = 2

                # center is pass work area
                if current_area_right == 4 and self.cycle_timer_status == 2:
                    self.cycle_is_pass_interested_area = True