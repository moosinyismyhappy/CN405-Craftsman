import sys
import threading
from PyQt5 import QtWidgets
from threading import Thread
from PyQt5.QtGui import QPixmap
from Gui_Project.GuiInputVideo import GuiInputVideo
from Gui_Project.GuiLayout import Ui_MainWindow
from Gui_Project.GuiOutputVideo import GuiOutputVideo

class GuiController(Thread):

    def __init__(self):
        super().__init__()
        self.thread_input_video = GuiInputVideo()
        self.thread_output_video = GuiOutputVideo(self.thread_input_video)
        self.count = 0

    def gui_processing(self):
        self.ui.pushButton.clicked.connect(self.open_camera_button)
        self.ui.pushButton_2.clicked.connect(self.close_camera_button)
        self.ui.pushButton_3.clicked.connect(self.exit_button)

    def open_camera_button(self):
        print('Open Camera Button Clicked...')
        self.thread_input_video.set_camera_status(True)
        self.thread_input_video.start()
        self.thread_output_video.start()
        self.thread_output_video.image_update.connect(self.image_update_slot)

    def image_update_slot(self, Image):
        self.ui.label.setPixmap(QPixmap.fromImage(Image))
        #self.count += 1
        #self.ui.label.setText(str(self.count))

    def close_camera_button(self):
        print('Close Camera Button Clicked...')
        self.thread_input_video.set_camera_status(False)

    def exit_button(self):
        sys.exit(0)

    def run(self):
        # Display Thread and Process ID
        print(threading.current_thread())
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)
        self.gui_processing()
        MainWindow.show()
        sys.exit(app.exec_())
