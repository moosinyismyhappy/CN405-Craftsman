import sys

from PyQt5 import QtWidgets

from Gui_Project.GuiController import GuiController
from Gui_Project.GuiLayout import Ui_MainWindow

if __name__ == "__main__":
    gui = GuiController()
    gui.start()
