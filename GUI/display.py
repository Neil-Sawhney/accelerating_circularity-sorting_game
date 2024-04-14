import logging
import sys

from PyQt5 import QtCore, QtWidgets, uic

import default_parameters as params
import game_logic.game as game
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


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.game_controller = game.Game(self)

        # Sets the maximum time to 180 seconds
        self.bar.setMaximum(180)

        # setup the GUI from the .ui file
        uic.loadUi("GUI/main.ui", self)

        self.set_info("PRESS THE FLASHING BUTTON TO BEGIN!")

    def set_info(self, text):
        self.info.setText(text)

    def set_score(self, score):
        self.score.display(score)

    def set_high_score(self, high_score):
        self.high_score.display(high_score)

    def set_time_left(self, time_left):
        self.bar.setValue(time_left)

    def update(self):
        self.game_controller.update()


def main():
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    app.exec_()
