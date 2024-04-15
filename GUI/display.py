import logging
import sys

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal

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


class GameThread(QThread):
    update_signal = pyqtSignal()  # signal to update the UI

    def __init__(self, game_controller):
        super(GameThread, self).__init__()
        self.game_controller = game_controller

    def run(self):
        while True:
            # Call your game logic function here
            self.game_controller.update()

            # Emit the signal to update the UI
            self.update_signal.emit()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # setup the GUI from the .ui file
        uic.loadUi("GUI/main.ui", self)

        # Sets the maximum time to 180 seconds
        self.bar.setMaximum(params.TIME_LIMIT)
        self.set_info("PRESS THE FLASHING BUTTON TO BEGIN!")

        self.game_controller = game.Game(self)

        # Start the game thread
        self.game_thread = GameThread(self.game_controller)
        self.game_thread.start()

    def set_info(self, text):
        self.info.setText(text)

    def set_score(self, score):
        self.score.display(score)

    def set_high_score(self, high_score):
        self.high_score.display(high_score)

    def set_time_left(self, time_left):
        self.bar.setValue(int(time_left))


def main():
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    app.exec_()
