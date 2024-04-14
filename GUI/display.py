import glob
import importlib
import logging
import os
import sys

import serial
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

import arduino.serial_rw as arduino
import default_parameters as params
import GUI.display_time as dTime
import GUI.error_display as eDisp

# logging
level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
logging.basicConfig(
    filename="./logs/debug.log",
    format="%(asctime)s|%(levelname)s|%(message)s",
    filemode="w",
    level=level[params.LOG_LEVEL],
)


def updateDefaultParameters(paramName, newValue):
    with open("./default_parameters.py", "r") as f:
        lines = f.readlines()
    with open("./default_parameters.py", "w") as f:
        for line in lines:
            if paramName in line:
                # if the value is a float, don't add quotes
                if isinstance(newValue, float):
                    f.write(paramName + " = " + str(newValue) + "\n")
                else:
                    f.write(paramName + ' = "' + newValue + '"\n')
            else:
                f.write(line)
    # reload the parameters
    importlib.reload(params)


def updateHighScore(newScore):
    try:
        os.remove("./logs/high_score.log")
    except FileNotFoundError:
        pass

    with open("./logs/high_score.log", "w") as f:
        f.write(str(newScore))


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # setup the GUI from the .ui file
        uic.loadUi("GUI/main.ui", self)

        arduino.init()

        while not arduino.check_ready():
            # set the info label to "Disconnected" until the arduino sends the ready signal
            self.info.setText("Initializing...")

        self.info.setText("PRESS THE FLASHING BUTTON TO BEGIN!")

    def update(self):
        T = dTime.getTime()
        data = arduino.readData()


def main():
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    app.exec_()
