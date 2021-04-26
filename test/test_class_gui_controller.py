from test_gui import *
import sys

class GuiController(Ui_MainWindow):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(MainWindow)

        # call other method from constructor
        self.processing()

        MainWindow.show()
        sys.exit(app.exec_())

    def processing(self):
        self.ui.pushButton.clicked.connect(self.open_camera_button)

    def open_camera_button(self):
        print('Open camera')
