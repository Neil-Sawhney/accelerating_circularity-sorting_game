import glob
import importlib
import logging
import sys

import serial
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

import arduino.serialRW as arduino
import defaultParameters as params
import GUI.displayTime as dTime
import GUI.errorDisplay as eDisp

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
    with open("./defaultParameters.py", "r") as f:
        lines = f.readlines()
    with open("./defaultParameters.py", "w") as f:
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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # setup the GUI from the .ui file
        uic.loadUi("GUI/main.ui", self)

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
