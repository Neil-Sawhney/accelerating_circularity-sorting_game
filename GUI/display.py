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

        # pages setup
        self.actionParameters.triggered.connect(self.Parameters)
        self.actionHome.triggered.connect(self.Home)

        # COM PORTS
        self.ports = self.comPorts()
        self.ports.append("None")
        self.arduinoDropdown.addItems(self.ports)
        self.arduinoDropdown.currentIndexChanged.connect(self.arduinoDropdownChanged)

    def update(self):
        T = dTime.getTime()
        data = arduino.readData()

    def Parameters(self):
        self.stackedWidget.setCurrentIndex(1)

    def Home(self):
        self.stackedWidget.setCurrentIndex(0)

    def arduinoDropdownChanged(self):
        updateDefaultParameters(
            "ARDUINO_COMPORT", self.ports[self.arduinoDropdown.currentIndex()]
        )

    def comPorts(self):

        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Unsupported platform")

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


def main():
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    app.exec_()
