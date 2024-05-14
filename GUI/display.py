import logging
import sys

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QFileInfo, QThread, QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSoundEffect

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
            self.game_controller.update()

            # Emit the signal to update the UI
            self.update_signal.emit()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # setup the GUI from the .ui file
        uic.loadUi("GUI/main.ui", self)

        # Makes the window fullscreen
        self.showFullScreen()

        # Sets the maximum time to 180 seconds
        self.bar.setMaximum(params.TIME_LIMIT)
        self.bar.setValue(params.TIME_LIMIT)

        self.set_info("INITIALIZING...")

        # set high_score_label and score_label to images
        high_score_image = QPixmap("assets/pics/high_score.png")
        score_image = QPixmap("assets/pics/score.png")
        self.high_score_label.setPixmap(high_score_image)
        self.score_label.setPixmap(score_image)

        # self.background_music = QSoundEffect()
        # self.background_music.setSource(
        #     QUrl.fromLocalFile(
        #         QFileInfo("assets/sounds/background_music.wav").absoluteFilePath()
        #     )
        # )
        # self.background_music.setVolume(0.1)
        # self.background_music.setLoopCount(-2)  # -2 is infinite for some reason...
        # self.background_music.play()

        self.correct_sound = QSoundEffect()
        self.correct_sound.setSource(
            QUrl.fromLocalFile(
                QFileInfo("assets/sounds/correct.wav").absoluteFilePath()
            )
        )
        self.wrong_sound = QSoundEffect()
        self.wrong_sound.setSource(
            QUrl.fromLocalFile(QFileInfo("assets/sounds/wrong.wav").absoluteFilePath())
        )
        self.scanned_sound = QSoundEffect()
        self.scanned_sound.setSource(
            QUrl.fromLocalFile(
                QFileInfo("assets/sounds/scanned.wav").absoluteFilePath()
            )
        )

        # Load the high score
        try:
            with open("./logs/high_score.log", "r") as f:
                high_score = int(f.read())
                self.set_high_score(high_score)
        except:
            logging.debug("Error reading high score file, setting high score to 0")
            high_score = 0
            pass

        self.game_controller = game.Game(self)

        # Start the game thread
        self.game_thread = GameThread(self.game_controller)
        self.game_thread.start()

    def set_info(self, text):
        self.info.setText(text)
        QtWidgets.QApplication.processEvents()

    def set_score(self, score):
        self.score.display(score)
        QtWidgets.QApplication.processEvents()

    def set_high_score(self, high_score):
        self.high_score.display(high_score)
        QtWidgets.QApplication.processEvents()

    def set_time_left(self, time_left):
        self.bar.setValue(int(time_left))
        QtWidgets.QApplication.processEvents()

    def play_correct_sound(self):
        self.correct_sound.play()

    def play_wrong_sound(self):
        self.wrong_sound.play()

    def play_scanned_sound(self):
        self.scanned_sound.play()


def main():
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()

    app.exec_()
