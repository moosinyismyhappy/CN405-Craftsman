import threading
import sys

from PyQt5.QtGui import QPixmap

from test_class_input_video import *
from test_class_output_video import *
from threading import Thread
from test_class_gui import *

class GuiController(Thread):

    def __init__(self):
        super().__init__()

    def setup_main_gui(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)

        # call other method from constructor
        self.processing()

        MainWindow.show()
        sys.exit(app.exec_())

    def processing(self):
        self.ui.pushButton.clicked.connect(self.open_camera_button)
        self.ui.pushButton_3.clicked.connect(self.exit_button)

    def open_camera_button(self):
        thread_input_video = InputVideo(0)
        thread_output_video = OutputVideo(thread_input_video)

        thread_input_video.start()
        thread_output_video.start()
        thread_output_video.ImageUpdate.connect(self.ImageUpdateSlot)


    def ImageUpdateSlot(self, Image):
        self.ui.label.setPixmap(QPixmap.fromImage(Image))

    def exit_button(self):
        sys.exit()

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())

        self.setup_main_gui()


